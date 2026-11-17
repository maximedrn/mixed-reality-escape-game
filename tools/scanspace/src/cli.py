"""Command-line entrypoint for ScanSpace architecture cleaning."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from zipfile import BadZipFile

from src.models.arguments import CleanArguments
from src.models.result import CleanResult
from src.services.architecture import clean_architecture
from src.utils.constants import (
    CLEAN,
    COMMAND_KEY,
    INPUT_OPTION,
    OUTPUT_OPTION,
    SCAN_OPTION,
    SCANSPACE,
)
from src.utils.messages import (
    BOUNDS_MESSAGE,
    CLEAN_HELP,
    CLEANED_FACES_MESSAGE,
    CLI_DESCRIPTION,
    GEOMETRY_MESSAGE,
    INPUT_HELP,
    ORIGINAL_FACES_MESSAGE,
    OUTPUT_HELP,
    OUTPUT_MESSAGE,
    SCAN_HELP,
    WINDOWS_MESSAGE,
)


def create_parser() -> ArgumentParser:
    """Configure the architecture-cleaning CLI and mandatory input paths.

    :return: CLI parser for the clean operation.
    :rtype: ArgumentParser
    """
    parser: ArgumentParser = ArgumentParser(
        prog=SCANSPACE,
        description=CLI_DESCRIPTION,
    )
    command: ArgumentParser = parser.add_subparsers(
        dest=COMMAND_KEY, required=True
    ).add_parser(CLEAN, help=CLEAN_HELP)
    command.add_argument(
        INPUT_OPTION, type=Path, required=True, help=INPUT_HELP
    )
    command.add_argument(
        SCAN_OPTION, type=Path, required=True, help=SCAN_HELP
    )
    command.add_argument(
        OUTPUT_OPTION, type=Path, required=True, help=OUTPUT_HELP
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the requested operation and print its export statistics.

    :param argv: Explicit CLI arguments or process arguments if None.
    :type argv: list[str] | None
    :return: No return value.
    :rtype: None
    """
    parser: ArgumentParser = create_parser()
    try:
        options: CleanArguments = CleanArguments.model_validate(
            vars(parser.parse_args(argv))
        )
        result: CleanResult = clean_architecture(options)
        print(OUTPUT_MESSAGE.format(output=result.output))
        print(
            ORIGINAL_FACES_MESSAGE.format(count=result.original_faces)
        )
        print(CLEANED_FACES_MESSAGE.format(count=result.clean_faces))
        print(WINDOWS_MESSAGE.format(count=result.windows_filled))
        print(BOUNDS_MESSAGE.format(bounds=result.bounds))
        print(GEOMETRY_MESSAGE.format(geometry=result.geometry))
    except (BadZipFile, KeyError, OSError, ValueError) as error:
        parser.error(str(error))
