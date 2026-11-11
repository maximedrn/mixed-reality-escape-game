"""Validate the TOML configuration with nested Pydantic models."""

from enum import StrEnum
from typing import Self

from pydantic import Field, field_validator, model_validator

from src.config.defaults import (
    A4_HEIGHT_MM,
    A4_WIDTH_MM,
    DEFAULT_GRID_GAP_MM,
    DEFAULT_GRID_MARGIN_MM,
    DEFAULT_OUTPUT_DIRECTORY,
    DEFAULT_PADDING_MM,
    DEFAULT_QR_SIZE_MM,
)
from src.models.base import FrozenModel
from src.models.entities import Layout
from src.utils.constants import (
    A4_GRID_PROFILE,
    AVERY_L7160_PROFILE,
    CUSTOM_PROFILE,
    GAME_ID_FIELD,
    OBJECT_ID_FIELD,
    ROOM_CONFIG_ID_FIELD,
    ROOM_ID_FIELD,
    ROOM_OBJECTS_FIELD,
)
from src.utils.messages import CUSTOM_LAYOUT_REQUIRED
from src.utils.validation import (
    validate_identifier,
)


class LabelProfile(StrEnum):
    """Name the supported sheet geometries."""

    AVERY_L7160 = AVERY_L7160_PROFILE  # noqa: TYP001, RUF100
    CUSTOM = CUSTOM_PROFILE  # noqa: TYP001, RUF100
    A4_GRID = A4_GRID_PROFILE  # noqa: TYP001, RUF100


class ProjectConfig(FrozenModel):
    """Identify the game encoded in every marker."""

    game_id: str

    @field_validator(GAME_ID_FIELD)
    @classmethod
    def validate_game_id(cls, value: str) -> str:
        """Validate the game identifier before accepting configuration.

        :param value: Configured game identifier.
        :return: Validated game identifier.
        """
        return validate_identifier(value, GAME_ID_FIELD)


class RoomConfig(FrozenModel):
    """List the physical objects belonging to one room."""

    id: str
    objects: list[str]

    @field_validator(ROOM_CONFIG_ID_FIELD)
    @classmethod
    def validate_room_id(cls, value: str) -> str:
        """Validate the room identifier.

        :param value: Configured room identifier.
        :return: Validated room identifier.
        """
        return validate_identifier(value, ROOM_ID_FIELD)

    @field_validator(ROOM_OBJECTS_FIELD)
    @classmethod
    def validate_object_ids(cls, values: list[str]) -> list[str]:
        """Validate every physical object identifier.

        :param values: Configured object identifiers.
        :return: Validated object identifiers in their original order.
        """
        return [
            validate_identifier(value, OBJECT_ID_FIELD) for value in values
        ]


class GridConfig(FrozenModel):
    """Describe an automatically sized page grid in millimeters."""

    page_width_mm: float = Field(default=A4_WIDTH_MM, gt=0)
    page_height_mm: float = Field(default=A4_HEIGHT_MM, gt=0)
    columns: int = Field(default=3, gt=0)
    rows: int = Field(default=7, gt=0)
    margin_x_mm: float = Field(default=DEFAULT_GRID_MARGIN_MM, ge=0)
    margin_y_mm: float = Field(default=DEFAULT_GRID_MARGIN_MM, ge=0)
    gap_x_mm: float = Field(default=DEFAULT_GRID_GAP_MM, ge=0)
    gap_y_mm: float = Field(default=DEFAULT_GRID_GAP_MM, ge=0)


class LabelsConfig(FrozenModel):
    """Select label geometry, captions and printer registration."""

    profile: LabelProfile = LabelProfile.AVERY_L7160
    custom: Layout | None = None
    grid: GridConfig = Field(default_factory=GridConfig)
    qr_size_mm: float = Field(default=DEFAULT_QR_SIZE_MM, gt=0)
    padding_mm: float = Field(default=DEFAULT_PADDING_MM, ge=0)
    start_index: int = Field(default=0, ge=0)
    show_text: bool = True
    draw_guides: bool = False
    shift_x_mm: float = 0.0
    shift_y_mm: float = 0.0

    @model_validator(mode="after")
    def validate_custom_profile(self: Self) -> Self:
        """Require measured geometry when a custom sheet is selected.

        :return: The validated label configuration.
        """
        if self.profile == LabelProfile.CUSTOM and self.custom is None:
            raise ValueError(CUSTOM_LAYOUT_REQUIRED)
        return self


class OutputConfig(FrozenModel):
    """Select SVG dimensions and a configuration-relative destination."""

    directory: str = DEFAULT_OUTPUT_DIRECTORY
    svg_size_mm: float = Field(default=DEFAULT_QR_SIZE_MM, gt=0)


class MarkerDefinitions(FrozenModel):
    """Describe the sections required to enumerate marker identities."""

    project: ProjectConfig
    rooms: list[RoomConfig]


class PrintConfiguration(FrozenModel):
    """Describe the section required to resolve print settings."""

    labels: LabelsConfig


class MarkerConfig(MarkerDefinitions, PrintConfiguration):
    """Describe a complete marker-generation configuration."""

    output: OutputConfig = Field(default_factory=OutputConfig)
