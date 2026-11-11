"""Command-line entrypoint for motion JSON preparation and GLB export."""

from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Callable
from pathlib import Path
from typing import Final

from src.config.defaults import DEFAULT_CONFIG
from src.config.settings import load_config, project_path
from src.models.arguments import (
    BuildArguments,
    Command,
    CommandArguments,
    ExportArguments,
    ValidateArguments,
)
from src.models.build import BuildRequest, BuildResult
from src.models.configuration import ProjectConfig
from src.models.motion import Motion
from src.services.build import build
from src.services.motion_io import export_motion, load_motion
from src.utils.constants import (
    ANIMATION_OPTION,
    BUILD,
    COMMAND_KEY,
    CONFIG,
    EXPORT_JSON,
    FPS_OPTION,
    INPUT,
    MODEL_OPTION,
    MOTION,
    OUTPUT_OPTION,
    VALIDATE,
)
from src.utils.messages import (
    ANIMATED_GLB_MESSAGE,
    CLI_DESCRIPTION,
    EXPORT_JSON_HELP,
    GENERATE_ANIMATED_GLB_HELP,
    JSON_EXPORTED_MESSAGE,
    MOTION_VALID_MESSAGE,
    OUTPUT_ANIMATED_GLB_PATH_HELP,
    VALIDATE_MOTION_JSON_HELP,
)

DEFAULT_FPS: Final[int] = 24


def create_parser() -> ArgumentParser:
    """Define the subcommands and their required arguments.

    :return: Define the subcommands and their required arguments.
    :rtype: ArgumentParser
    """
    parser: ArgumentParser = ArgumentParser(
        prog=MOTION,
        description=CLI_DESCRIPTION,
    )
    add_command: Callable[..., ArgumentParser] = parser.add_subparsers(
        dest=COMMAND_KEY, required=True
    ).add_parser
    generate: ArgumentParser = add_command(
        BUILD, help=GENERATE_ANIMATED_GLB_HELP
    )
    generate.add_argument(CONFIG, type=Path, default=DEFAULT_CONFIG)
    generate.add_argument(MODEL_OPTION, type=Path)
    generate.add_argument(ANIMATION_OPTION, type=Path)
    generate.add_argument(
        OUTPUT_OPTION, type=Path, help=OUTPUT_ANIMATED_GLB_PATH_HELP
    )
    importer: ArgumentParser = add_command(EXPORT_JSON, help=EXPORT_JSON_HELP)
    importer.add_argument(INPUT, type=Path, required=True)
    importer.add_argument(MODEL_OPTION, type=Path, required=True)
    importer.add_argument(OUTPUT_OPTION, type=Path, required=True)
    importer.add_argument(FPS_OPTION, type=int, default=DEFAULT_FPS)
    check: ArgumentParser = add_command(
        VALIDATE, help=VALIDATE_MOTION_JSON_HELP
    )
    check.add_argument(ANIMATION_OPTION, type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the selected command and display its verified result.

    :param argv: Explicit arguments, or None for process arguments.
    :type argv: list[str] | None
    :return: No return value.
    :rtype: None
    """
    parser: ArgumentParser = create_parser()
    raw: dict[str, object] = vars(parser.parse_args(argv))
    try:
        command: Command = CommandArguments.model_validate(
            {COMMAND_KEY: raw[COMMAND_KEY]}
        ).command
        if command == Command.EXPORT_JSON:
            arguments: ExportArguments = ExportArguments.model_validate(raw)
            motion: Motion = export_motion(
                arguments.input,
                arguments.model,
                arguments.output,
                arguments.fps,
            )
            print(
                JSON_EXPORTED_MESSAGE.format(
                    output=arguments.output,
                    frame_count=motion.frame_count,
                    marker_count=len(motion.markers),
                    bone_count=len(motion.rig_pose.bone_names),
                )
            )
        elif command == Command.VALIDATE:
            validation: ValidateArguments = ValidateArguments.model_validate(
                raw
            )
            motion = load_motion(validation.animation)
            print(
                MOTION_VALID_MESSAGE.format(
                    name=motion.clip.name,
                    frame_count=motion.frame_count,
                    fps=motion.clip.fps,
                )
            )
        else:
            options: BuildArguments = BuildArguments.model_validate(raw)
            config_file: Path = options.config.expanduser().resolve()
            cfg: ProjectConfig = load_config(config_file)
            model: Path = options.model or project_path(
                config_file, cfg.inputs.model
            )
            animation: Path = options.animation or project_path(
                config_file, cfg.inputs.animation
            )
            glb: Path = options.output or project_path(
                config_file, cfg.outputs.glb
            )
            result: BuildResult = build(
                BuildRequest(
                    model=model.resolve(),
                    animation=animation.resolve(),
                    output_glb=glb.resolve(),
                )
            )
            print(ANIMATED_GLB_MESSAGE.format(glb=result.glb))
    except (OSError, ValueError, RuntimeError) as error:
        parser.error(str(error))
