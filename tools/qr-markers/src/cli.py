"""Expose marker generation as a typed command-line application."""

from argparse import ArgumentParser
from pathlib import Path

from src.services.generation import generate
from src.utils.constants import (
    CONFIG_OPTION,
    PDF_FILENAME,
)
from src.utils.messages import (
    CLI_CONFIG_HELP,
    CLI_DESCRIPTION,
    GENERATED_MESSAGE,
)


def create_parser() -> ArgumentParser:
    """Create the marker command parser.

    :return: Parser for the required TOML configuration.
    """
    parser: ArgumentParser = ArgumentParser(
        description=CLI_DESCRIPTION, allow_abbrev=False
    )
    parser.add_argument(
        CONFIG_OPTION,
        type=Path,
        required=True,
        help=CLI_CONFIG_HELP,
    )
    return parser


def main() -> None:
    """Generate marker exports from the supplied TOML file.

    :raises SystemExit: With status 2 for invalid options or configuration.
    """
    parser: ArgumentParser = create_parser()
    count: int
    destination: Path
    try:
        config: Path = parser.parse_args().config
        count, destination = generate(config)
    except (KeyError, OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(
        GENERATED_MESSAGE.format(
            count=count, destination=destination / PDF_FILENAME
        )
    )
