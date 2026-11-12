"""Plan named clip exports and validate the whole batch before publication."""

from pathlib import Path

from src.config.settings import load_config, project_path
from src.models.arguments import BuildArguments
from src.models.build import BuildRequest, BuildResult, PreparedBuild
from src.models.configuration import AnimationConfig, ProjectConfig
from src.services.build import prepare_build, publish_build
from src.utils.messages import (
    AMBIGUOUS_OVERRIDE_ERROR,
    BUILD_DESTINATIONS_ERROR,
    DUPLICATE_OUTPUTS_ERROR,
    UNKNOWN_ANIMATION_ERROR,
)


def build_project(options: BuildArguments) -> list[BuildResult]:
    """Validate all selected inputs, then publish each verified GLB.

    :param options: Configuration path, optional clip name and path overrides.
    :type options: BuildArguments
    :return: Published outputs in configuration order.
    :rtype: list[BuildResult]
    """
    requests: list[BuildRequest] = plan_builds(options)
    prepared: list[PreparedBuild] = [
        prepare_build(request) for request in requests
    ]
    return [publish_build(item) for item in prepared]


def plan_builds(options: BuildArguments) -> list[BuildRequest]:
    """Resolve selected clips and reject destructive destination collisions.

    :param options: CLI configuration and explicit overrides.
    :type options: BuildArguments
    :return: Existing inputs and distinct output paths for every selected clip.
    :rtype: list[BuildRequest]
    """
    file: Path = options.config.expanduser().resolve()
    config: ProjectConfig = load_config(file)
    animations: list[AnimationConfig] = config.animations
    if animations and options.name is not None:
        animations = [
            animation
            for animation in animations
            if animation.name == options.name
        ]
        if not animations:
            raise ValueError(UNKNOWN_ANIMATION_ERROR.format(name=options.name))
    if len(animations) > 1 and (
        options.animation is not None or options.output is not None
    ):
        raise ValueError(AMBIGUOUS_OVERRIDE_ERROR)
    model: Path = (
        (options.model or project_path(file, config.inputs.model))
        .expanduser()
        .resolve()
    )
    constraints: Path | None = (
        project_path(file, config.inputs.constraints).resolve()
        if config.inputs.constraints is not None
        else None
    )
    requests: list[BuildRequest] = []
    animation: AnimationConfig
    if animations:
        for animation in animations:
            requests.append(
                BuildRequest(
                    model=model,
                    constraints=constraints,
                    name=animation.name,
                    animation=(
                        options.animation
                        or project_path(file, animation.input)
                    )
                    .expanduser()
                    .resolve(),
                    output_glb=(
                        options.output or project_path(file, animation.output)
                    )
                    .expanduser()
                    .resolve(),
                )
            )
    else:
        requests.append(
            BuildRequest(
                model=model,
                constraints=constraints,
                name=options.name,
                animation=(
                    options.animation
                    or project_path(file, config.inputs.animation)
                )
                .expanduser()
                .resolve(),
                output_glb=(
                    options.output or project_path(file, config.outputs.glb)
                )
                .expanduser()
                .resolve(),
            )
        )
    destinations: list[str] = [
        str(request.output_glb).casefold() for request in requests
    ]
    if len(destinations) != len(set(destinations)):
        raise ValueError(DUPLICATE_OUTPUTS_ERROR)
    sources: set[str] = {str(file).casefold(), str(model).casefold()}
    if constraints is not None:
        sources.add(str(constraints).casefold())
    sources.update(str(request.animation).casefold() for request in requests)
    sources.update(
        str(project_path(file, animation.input).resolve()).casefold()
        for animation in config.animations
    )
    if sources.intersection(destinations):
        raise ValueError(BUILD_DESTINATIONS_ERROR)
    return requests
