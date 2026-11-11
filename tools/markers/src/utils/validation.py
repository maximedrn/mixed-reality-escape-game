"""Validate marker identifiers and command-line grid dimensions."""

from re import Match, fullmatch
from typing import Final

from src.utils.constants import GRID_PATTERN, IDENTIFIER_PATTERN
from src.utils.messages import GRID_ERROR, IDENTIFIER_ERROR

GRID_ROWS_GROUP: Final[int] = 2


def validate_identifier(value: object, field: str) -> str:
    """Validate one payload component without changing its value.

    :param value: Input value to validate.
    :param field: Field name for validation errors.
    :return: The validated identifier.
    :raises ValueError: If the supplied values are invalid.
    """
    if not isinstance(value, str) or not fullmatch(IDENTIFIER_PATTERN, value):
        raise ValueError(IDENTIFIER_ERROR.format(field=field, value=value))
    return value


def parse_grid(value: str) -> tuple[int, int]:
    """Parse a positive column and row count from COLSxROWS.

    :param value: Input value to validate.
    :return: Positive column and row counts.
    :raises ValueError: If the supplied values are invalid.
    """
    match: Match[str] | None = fullmatch(GRID_PATTERN, value)
    if match is None:
        raise ValueError(GRID_ERROR)
    return int(match[1]), int(match[GRID_ROWS_GROUP])
