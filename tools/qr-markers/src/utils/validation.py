"""Validate marker identifiers."""

from re import fullmatch

from src.utils.constants import IDENTIFIER_PATTERN
from src.utils.messages import IDENTIFIER_ERROR


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
