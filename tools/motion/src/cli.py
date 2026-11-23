"""Command-line entrypoint for motion JSON preparation and GLB export."""

from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from pathlib import Path

from src.config.settings import load_config, project_path
from src.models.build import BuildResult
from src.models.configuration import ExportConfig, ValidateConfig
from src.models.motion import Motion
from src.services.motion_io import export_motion, load_motion
from src.services.project import build_project
from src.utils.constants import (
    BUILD,
    COMMAND_KEY,
    CONFIG,
    EXPORT_JSON,
    MOTION,
    VALIDATE,
)
from src.utils.messages import (
    ANIMATED_GLB_MESSAGE,
    BUILD_DESTINATIONS_ERROR,
    CLI_DESCRIPTION,
    CONFIG_HELP,
    CONSTRAINT_SAMPLES_MESSAGE,
    EXPORT_JSON_HELP,
    GENERATE_ANIMATED_GLB_HELP,
    JSON_EXPORTED_MESSAGE,
    MOTION_VALID_MESSAGE,
    VALIDATE_MOTION_JSON_HELP,
)


def create_parser() -> ArgumentParser:
    """Define the operations and their required TOML file.

    :return: Motion command parser.
    :rtype: ArgumentParser
    """
    parser: ArgumentParser = ArgumentParser(
        prog=MOTION, description=CLI_DESCRIPTION, allow_abbrev=False
    )
    add_command: Callable[..., ArgumentParser] = parser.add_subparsers(
        dest=COMMAND_KEY, required=True
    ).add_parser
    for name, help_text in (
        (BUILD, GENERATE_ANIMATED_GLB_HELP),
        (EXPORT_JSON, EXPORT_JSON_HELP),
        (VALIDATE, VALIDATE_MOTION_JSON_HELP),
    ):
        command: ArgumentParser = add_command(
            name, help=help_text, allow_abbrev=False
        )
        command.add_argument(
            CONFIG, type=Path, required=True, help=CONFIG_HELP
        )
    return parser


def main() -> None:
    """Run the selected operation using its TOML configuration.

    :return: No return value.
    :rtype: None
    """
    parser: ArgumentParser = create_parser()
    arguments: Namespace = parser.parse_args()
    try:
        file: Path = arguments.config.expanduser().resolve()
        if arguments.command == EXPORT_JSON:
            settings: ExportConfig = load_config(file, ExportConfig)
            animation: Path = project_path(file, settings.input)
            model: Path = project_path(file, settings.model)
            output: Path = project_path(file, settings.output)
            if output in (file, animation, model):
                raise ValueError(BUILD_DESTINATIONS_ERROR)
            motion: Motion = export_motion(
                animation, model, output, settings.fps
            )
            print(
                JSON_EXPORTED_MESSAGE.format(
                    output=output,
                    frame_count=motion.frame_count,
                    marker_count=len(motion.markers),
                    bone_count=len(motion.rig_pose.bone_names),
                )
            )
        elif arguments.command == VALIDATE:
            validation: ValidateConfig = load_config(file, ValidateConfig)
            motion = load_motion(project_path(file, validation.animation))
            print(
                MOTION_VALID_MESSAGE.format(
                    name=motion.clip.name,
                    frame_count=motion.frame_count,
                    fps=motion.clip.fps,
                )
            )
        else:
            result: BuildResult
            for result in build_project(file):
                print(ANIMATED_GLB_MESSAGE.format(glb=result.glb))
                if result.constrained_samples:
                    print(
                        CONSTRAINT_SAMPLES_MESSAGE.format(
                            count=result.constrained_samples
                        )
                    )
    except (OSError, ValueError, RuntimeError) as error:
        parser.error(str(error))
