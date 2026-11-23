"""CLI for FreeMoCap batch capture processing."""

from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from pathlib import Path

from src.models.runtime import Batch, JobResult
from src.services.configuration import load_configuration
from src.services.runner import run_batch
from src.services.validation import validate_batch
from src.utils.constants import (
    APPLICATION,
    BUILD,
    COMMAND_KEY,
    CONFIG_OPTION,
    STATUS_FAILED,
    VALIDATE,
)
from src.utils.messages import (
    BUILD_HELP,
    CAMERA_ASSIGNMENT,
    CAMERA_ASSIGNMENT_ITEM,
    CAMERA_ASSIGNMENT_SEPARATOR,
    CLI_DESCRIPTION,
    CONFIG_HELP,
    RESULT_SUMMARY,
    VALIDATE_HELP,
    VALIDATED,
)


def create_parser() -> ArgumentParser:
    """Define the operations and their required TOML file.

    :return: FreeMoCap batch command parser.
    :rtype: ArgumentParser
    """
    parser: ArgumentParser = ArgumentParser(
        prog=APPLICATION, description=CLI_DESCRIPTION, allow_abbrev=False
    )
    add_command: Callable[..., ArgumentParser] = parser.add_subparsers(
        dest=COMMAND_KEY, required=True
    ).add_parser
    for name, help_text in ((VALIDATE, VALIDATE_HELP), (BUILD, BUILD_HELP)):
        command: ArgumentParser = add_command(
            name, help=help_text, allow_abbrev=False
        )
        command.add_argument(
            CONFIG_OPTION, type=Path, required=True, help=CONFIG_HELP
        )
    return parser


def main() -> None:
    """Validate or process animations from the supplied TOML file.

    :return: No return value.
    :rtype: None
    """
    parser: ArgumentParser = create_parser()
    options: Namespace = parser.parse_args()
    try:
        batch: Batch = load_configuration(options.config)
        validate_batch(batch)
        for job in batch.jobs:
            cameras: str = CAMERA_ASSIGNMENT_SEPARATOR.join(
                CAMERA_ASSIGNMENT_ITEM.format(
                    camera=video.camera, filename=video.path.name
                )
                for video in job.videos
            )
            print(CAMERA_ASSIGNMENT.format(name=job.name, cameras=cameras))
        if options.command == VALIDATE:
            print(VALIDATED.format(count=len(batch.jobs)))
            return
        results: list[JobResult] = run_batch(batch)
        failed: int = sum(result.status == STATUS_FAILED for result in results)
        print(
            RESULT_SUMMARY.format(
                success=len(results) - failed,
                failed=failed,
            )
        )
        if failed:
            raise SystemExit(1)
    except (OSError, RuntimeError, ValueError) as error:
        parser.error(str(error))
