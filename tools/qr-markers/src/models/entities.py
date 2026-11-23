"""Represent spatial marker identifiers and physical sheet geometry."""

from typing import Self

from pydantic import ValidationInfo, field_validator, model_validator

from src.models.base import FrozenModel
from src.utils.constants import (
    EMPTY_TEXT,
    GAME_ID_FIELD,
    GEOMETRY_EPSILON,
    MARKER_FILENAME_TEMPLATE,
    MARKER_PAYLOAD_TEMPLATE,
    OBJECT_ID_FIELD,
    ROOM_ID_FIELD,
)
from src.utils.messages import (
    GRID_DIMENSIONS_ERROR,
    PAGE_DIMENSIONS_ERROR,
    PAGE_HEIGHT_ERROR,
    PAGE_SPACING_ERROR,
    PAGE_WIDTH_ERROR,
)
from src.utils.validation import validate_identifier


class Marker(FrozenModel):
    """Identify one physical object within a game and room.

    :param game_id: Game identifier.
    :param room_id: Room identifier.
    :param object_id: Physical object identifier.
    """

    game_id: str
    room_id: str
    object_id: str

    @field_validator(GAME_ID_FIELD, ROOM_ID_FIELD, OBJECT_ID_FIELD)
    @classmethod
    def validate_identity(cls, value: str, info: ValidationInfo) -> str:
        """Validate one identity component using its model field name.

        :param value: Identifier component.
        :param info: Pydantic validation context containing the field name.
        :return: Validated identifier component.
        """
        return validate_identifier(value, info.field_name or EMPTY_TEXT)

    @property
    def payload(self: Self) -> str:
        """Return the exact ASCII payload encoded in the QR code.

        :return: The colon-separated game, room and object identifiers.
        """
        return MARKER_PAYLOAD_TEMPLATE.format(
            game_id=self.game_id,
            room_id=self.room_id,
            object_id=self.object_id,
        )

    @property
    def filename(self: Self) -> str:
        """Return the stable SVG filename for this marker.

        :return: The room and object identifiers with an SVG extension.
        """
        return MARKER_FILENAME_TEMPLATE.format(
            room_id=self.room_id, object_id=self.object_id
        )


class Layout(FrozenModel):
    """Describe page and label dimensions in millimeters.

    :param page_width_mm: Page width in millimeters.
    :param page_height_mm: Page height in millimeters.
    :param columns: Number of label columns.
    :param rows: Number of label rows.
    :param label_width_mm: Label width in millimeters.
    :param label_height_mm: Label height in millimeters.
    :param margin_left_mm: Left page margin.
    :param margin_top_mm: Top page margin.
    :param gap_x_mm: Horizontal spacing between labels.
    :param gap_y_mm: Vertical spacing between labels.
    """

    page_width_mm: float
    page_height_mm: float
    columns: int
    rows: int
    label_width_mm: float
    label_height_mm: float
    margin_left_mm: float
    margin_top_mm: float
    gap_x_mm: float
    gap_y_mm: float

    @property
    def capacity(self: Self) -> int:
        """Return the number of available positions on each page.

        :return: The number of label positions.
        """
        return self.columns * self.rows

    @model_validator(mode="after")
    def validate_geometry(self: Self) -> Self:
        """Reject dimensions or offsets that cannot fit on the sheet.

        :return: The validated sheet geometry.
        :raises ValueError: If the supplied values are invalid.
        """
        if self.columns < 1 or self.rows < 1:
            raise ValueError(GRID_DIMENSIONS_ERROR)
        dimensions: tuple[float, ...] = (
            self.page_width_mm,
            self.page_height_mm,
            self.label_width_mm,
            self.label_height_mm,
        )
        if any(dimension <= 0 for dimension in dimensions):
            raise ValueError(PAGE_DIMENSIONS_ERROR)
        if any(
            offset < 0
            for offset in (
                self.margin_left_mm,
                self.margin_top_mm,
                self.gap_x_mm,
                self.gap_y_mm,
            )
        ):
            raise ValueError(PAGE_SPACING_ERROR)

        occupied_width: float = (
            self.margin_left_mm
            + self.columns * self.label_width_mm
            + (self.columns - 1) * self.gap_x_mm
        )
        occupied_height: float = (
            self.margin_top_mm
            + self.rows * self.label_height_mm
            + (self.rows - 1) * self.gap_y_mm
        )
        if occupied_width > self.page_width_mm + GEOMETRY_EPSILON:
            raise ValueError(PAGE_WIDTH_ERROR)
        if occupied_height > self.page_height_mm + GEOMETRY_EPSILON:
            raise ValueError(PAGE_HEIGHT_ERROR)
        return self
