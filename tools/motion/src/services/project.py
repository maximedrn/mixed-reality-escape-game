"""Plan clip exports and validate the whole batch before publication."""

from pathlib import Path

from src.config.settings import load_config, project_path
from src.models.build import BuildRequest, BuildResult, PreparedBuild
from src.models.configuration import ProjectConfig
from src.services.build import prepare_build, publish_build
from src.utils.messages import (
    BUILD_DESTINATIONS_ERROR,
    DUPLICATE_OUTPUTS_ERROR,
    SINGLE_CLIP_PATHS_REQUIRED,
)


def build_project(file: Path) -> list[BuildResult]:
    """Validate all configured inputs, then publish each verified GLB.

    :param file: TOML file defining the rig, clips and GLB destinations.
    :type file: Path
    :return: Published outputs in configuration order.
    :rtype: list[BuildResult]
    """
    requests: list[BuildRequest] = plan_builds(file)
    prepared: list[PreparedBuild] = [
        prepare_build(request) for request in requests
    ]
    return [publish_build(item) for item in prepared]


def plan_builds(file: Path) -> list[BuildRequest]:
    """Resolve configured clips and reject destructive destination collisions.

    :param file: TOML file defining the rig, clips and GLB destinations.
    :type file: Path
    :return: Existing inputs and distinct output paths for every clip.
    :rtype: list[BuildRequest]
    """
    file = file.expanduser().resolve()
    config: ProjectConfig = load_config(file, ProjectConfig)
    model: Path = project_path(file, config.inputs.model)
    constraints: Path | None = (
        project_path(file, config.inputs.constraints)
        if config.inputs.constraints is not None
        else None
    )
    requests: list[BuildRequest]
    if config.animations:
        requests = [
            BuildRequest(
                model=model,
                constraints=constraints,
                name=animation.name,
                animation=project_path(file, animation.input),
                output_glb=project_path(file, animation.output),
            )
            for animation in config.animations
        ]
    else:
        if config.inputs.animation is None or config.outputs.glb is None:
            raise ValueError(SINGLE_CLIP_PATHS_REQUIRED)
        requests = [
            BuildRequest(
                model=model,
                constraints=constraints,
                name=None,
                animation=project_path(file, config.inputs.animation),
                output_glb=project_path(file, config.outputs.glb),
            )
        ]

    destinations: list[str] = [
        str(request.output_glb).casefold() for request in requests
    ]
    if len(destinations) != len(set(destinations)):
        raise ValueError(DUPLICATE_OUTPUTS_ERROR)
    sources: set[str] = {str(file).casefold(), str(model).casefold()}
    if constraints is not None:
        sources.add(str(constraints).casefold())
    sources.update(str(request.animation).casefold() for request in requests)
    if sources.intersection(destinations):
        raise ValueError(BUILD_DESTINATIONS_ERROR)
    return requests
