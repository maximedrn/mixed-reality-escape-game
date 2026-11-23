"""Validate the small subset of ScanSpace metadata used for window fills."""

from typing import ClassVar

from pydantic import ConfigDict, Field, field_validator

from src.models.base import FrozenModel
from src.utils.constants import DIMENSIONS_FIELD, IGNORE, TRANSFORM_ELEMENTS
from src.utils.messages import INVALID_WINDOW_DIMENSIONS_ERROR


class WindowDefinition(FrozenModel):
    """Represent one RoomPlan window with its local size and world pose."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra=IGNORE)

    transform: tuple[float, ...] = Field(
        min_length=TRANSFORM_ELEMENTS,
        max_length=TRANSFORM_ELEMENTS,
    )
    dimensions: tuple[float, float, float]

    @field_validator(DIMENSIONS_FIELD)
    @classmethod
    def validate_dimensions(
        cls, value: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """Reject non-positive window widths and heights.

        :param value: Window width, height and depth in metres.
        :type value: tuple[float, float, float]
        :return: Validated dimensions.
        :rtype: tuple[float, float, float]
        """
        if value[0] <= 0 or value[1] <= 0:
            raise ValueError(INVALID_WINDOW_DIMENSIONS_ERROR)
        return value


class ScanStructure(FrozenModel):
    """Extract window metadata while allowing unrelated RoomPlan fields."""

    model_config: ClassVar[ConfigDict] = ConfigDict(extra=IGNORE)

    windows: list[WindowDefinition]
