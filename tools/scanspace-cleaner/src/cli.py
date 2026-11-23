"""Command-line entrypoint for ScanSpace architecture cleaning."""

from argparse import ArgumentParser
from pathlib import Path
from zipfile import BadZipFile

from src.models.result import CleanResult
from src.services.architecture import clean_architecture
from src.utils.constants import CLEAN, CONFIG_OPTION, SCANSPACE
from src.utils.messages import (
    BOUNDS_MESSAGE,
    CLEAN_HELP,
    CLEANED_FACES_MESSAGE,
    CLI_DESCRIPTION,
    CONFIG_HELP,
    GEOMETRY_MESSAGE,
    ORIGINAL_FACES_MESSAGE,
    OUTPUT_MESSAGE,
    WINDOWS_MESSAGE,
)


def create_parser() -> ArgumentParser:
    """Configure the clean operation and its required TOML file.

    :return: CLI parser for the clean operation.
    :rtype: ArgumentParser
    """
    parser: ArgumentParser = ArgumentParser(
        prog=SCANSPACE, description=CLI_DESCRIPTION, allow_abbrev=False
    )
    command: ArgumentParser = parser.add_subparsers(required=True).add_parser(
        CLEAN, help=CLEAN_HELP, allow_abbrev=False
    )
    command.add_argument(
        CONFIG_OPTION, type=Path, required=True, help=CONFIG_HELP
    )
    return parser


def main() -> None:
    """Clean the configured scan and print its export statistics.

    :return: No return value.
    :rtype: None
    """
    parser: ArgumentParser = create_parser()
    try:
        config: Path = parser.parse_args().config
        result: CleanResult = clean_architecture(config)
        print(OUTPUT_MESSAGE.format(output=result.output))
        print(ORIGINAL_FACES_MESSAGE.format(count=result.original_faces))
        print(CLEANED_FACES_MESSAGE.format(count=result.clean_faces))
        print(WINDOWS_MESSAGE.format(count=result.windows_filled))
        print(BOUNDS_MESSAGE.format(bounds=result.bounds))
        print(GEOMETRY_MESSAGE.format(geometry=result.geometry))
    except (BadZipFile, KeyError, OSError, ValueError) as error:
        parser.error(str(error))
