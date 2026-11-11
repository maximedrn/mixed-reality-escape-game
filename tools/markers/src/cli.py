"""Expose marker generation as a typed command-line application."""

from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

from src.config.defaults import DEFAULT_CONFIG_PATH
from src.models.base import FrozenModel
from src.services.generation import generate
from src.utils.constants import (
    CONFIG_OPTION,
    GRID_METAVAR,
    GRID_OPTION,
    OUTPUT_OPTION,
    PDF_FILENAME,
)
from src.utils.messages import (
    CLI_CONFIG_HELP,
    CLI_DESCRIPTION,
    CLI_GRID_HELP,
    CLI_OUTPUT_HELP,
    GENERATED_MESSAGE,
)
from src.utils.validation import parse_grid


class CliArguments(FrozenModel):
    """Describe parsed marker-generation options.

    :param config: TOML configuration path.
    :param output: Optional export destination override.
    :param grid: Optional column and row counts.
    """

    config: Path
    output: Path | None
    grid: tuple[int, int] | None


def _grid_argument(value: str) -> tuple[int, int]:
    """Translate grid validation failures into argparse errors.

    :param value: Grid expressed as COLSxROWS.
    :return: Positive column and row counts.
    :raises ArgumentTypeError: If the grid syntax is invalid.
    """
    try:
        return parse_grid(value)
    except ValueError as error:
        raise ArgumentTypeError(str(error)) from error


def create_parser() -> ArgumentParser:
    """Create the marker command parser.

    :return: Parser for configuration, output and grid options.
    """
    parser: ArgumentParser = ArgumentParser(description=CLI_DESCRIPTION)
    parser.add_argument(
        CONFIG_OPTION,
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=CLI_CONFIG_HELP,
    )
    parser.add_argument(OUTPUT_OPTION, type=Path, help=CLI_OUTPUT_HELP)
    parser.add_argument(
        GRID_OPTION,
        type=_grid_argument,
        metavar=GRID_METAVAR,
        help=CLI_GRID_HELP,
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Parse command-line options and generate all marker exports.

    :param argv: Arguments to parse, or None for the process arguments.
    :raises SystemExit: With status 2 for invalid options or configuration.
    """
    parser: ArgumentParser = create_parser()
    count: int
    destination: Path
    try:
        arguments: CliArguments = CliArguments.model_validate(
            vars(parser.parse_args(argv))
        )
        count, destination = generate(
            arguments.config, arguments.output, arguments.grid
        )
    except (KeyError, OSError, TypeError, ValueError) as error:
        parser.error(str(error))
    print(
        GENERATED_MESSAGE.format(
            count=count, destination=destination / PDF_FILENAME
        )
    )
