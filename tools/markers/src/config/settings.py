"""Load marker definitions, label presets and printer settings."""

from collections.abc import Mapping
from typing import Final, Self

from pydantic import model_validator

from src.config.defaults import (
    A4_HEIGHT_MM,
    A4_WIDTH_MM,
    AVERY_GAP_X_MM,
    AVERY_LABEL_HEIGHT_MM,
    AVERY_LABEL_WIDTH_MM,
    AVERY_MARGIN_LEFT_MM,
    AVERY_MARGIN_TOP_MM,
)
from src.models.base import FrozenModel
from src.models.configuration import (
    GridConfig,
    LabelProfile,
    LabelsConfig,
    MarkerConfig,
    MarkerDefinitions,
    PrintConfiguration,
)
from src.models.entities import Layout, Marker
from src.utils.constants import GEOMETRY_EPSILON, PADDING_SIDES
from src.utils.messages import (
    CONFLICTING_FILENAME_ERROR,
    CUSTOM_LAYOUT_REQUIRED,
    DUPLICATE_MARKER_ERROR,
    GRID_DIMENSIONS_ERROR,
    NO_OBJECTS_ERROR,
    PRINTER_OFFSETS_ERROR,
    QR_DIMENSIONS_ERROR,
    QR_FIT_ERROR,
    START_INDEX_ERROR,
)

AVERY_L7160: Final[Layout] = Layout(
    page_width_mm=A4_WIDTH_MM,
    page_height_mm=A4_HEIGHT_MM,
    columns=3,
    rows=7,
    label_width_mm=AVERY_LABEL_WIDTH_MM,
    label_height_mm=AVERY_LABEL_HEIGHT_MM,
    margin_left_mm=AVERY_MARGIN_LEFT_MM,
    margin_top_mm=AVERY_MARGIN_TOP_MM,
    gap_x_mm=AVERY_GAP_X_MM,
    gap_y_mm=0.0,
)


class LabelSettings(FrozenModel):
    """Configure a label layout, captions and printer offsets.

    :param layout: Physical sheet geometry.
    :param qr_size_mm: QR width including the quiet zone.
    :param padding_mm: Space between the label edge and its QR.
    :param start_index: Positions already used on the first sheet.
    :param show_text: Whether to include readable identification text.
    :param draw_guides: Whether to draw label borders.
    :param shift_x_mm: Horizontal printer registration offset.
    :param shift_y_mm: Vertical printer registration offset.
    """

    layout: Layout
    qr_size_mm: float
    padding_mm: float
    start_index: int = 0
    show_text: bool = True
    draw_guides: bool = False
    shift_x_mm: float = 0.0
    shift_y_mm: float = 0.0

    @model_validator(mode="after")
    def validate_geometry(self: Self) -> Self:
        """Reject dimensions or offsets that cannot fit on the sheet.

        :return: The validated sheet geometry.
        :raises ValueError: If the supplied values are invalid.
        """
        if self.padding_mm < 0 or self.qr_size_mm <= 0:
            raise ValueError(QR_DIMENSIONS_ERROR)
        if self.qr_size_mm + PADDING_SIDES * self.padding_mm > min(
            self.layout.label_width_mm, self.layout.label_height_mm
        ):
            raise ValueError(QR_FIT_ERROR)
        if not 0 <= self.start_index < self.layout.capacity:
            raise ValueError(START_INDEX_ERROR)

        # Printer registration offsets may be negative but cannot move labels
        # beyond the physical sheet (including the QR and its quiet zone).
        right: float = (
            self.layout.margin_left_mm
            + self.layout.columns * self.layout.label_width_mm
            + (self.layout.columns - 1) * self.layout.gap_x_mm
        )
        bottom: float = (
            self.layout.margin_top_mm
            + self.layout.rows * self.layout.label_height_mm
            + (self.layout.rows - 1) * self.layout.gap_y_mm
        )
        if not (
            0 <= self.layout.margin_left_mm + self.shift_x_mm
            and right + self.shift_x_mm
            <= self.layout.page_width_mm + GEOMETRY_EPSILON
            and 0 <= self.layout.margin_top_mm + self.shift_y_mm
            and bottom + self.shift_y_mm
            <= self.layout.page_height_mm + GEOMETRY_EPSILON
        ):
            raise ValueError(PRINTER_OFFSETS_ERROR)

        return self


def load_markers(
    data: MarkerDefinitions | Mapping[str, object],
) -> list[Marker]:
    """Validate configuration and load unique marker identities.

    :param data: Marker definitions or configuration decoded from TOML.
    :return: Markers in configuration order.
    :raises ValueError: If identifiers are invalid or duplicated.
    """
    definitions: MarkerDefinitions
    if isinstance(data, MarkerDefinitions):
        definitions = data
    elif set(data).issubset(MarkerDefinitions.model_fields):
        definitions = MarkerDefinitions.model_validate(data)
    else:
        definitions = MarkerConfig.model_validate(data)
    markers: list[Marker] = []
    identifiers: set[tuple[str, str]] = set()
    filenames: set[str] = set()
    for room in definitions.rooms:
        for object_id in room.objects:
            marker: Marker = Marker(
                game_id=definitions.project.game_id,
                room_id=room.id,
                object_id=object_id,
            )
            identifier: tuple[str, str] = (room.id, object_id)
            if identifier in identifiers:
                raise ValueError(
                    DUPLICATE_MARKER_ERROR.format(payload=marker.payload)
                )
            if marker.filename in filenames:
                raise ValueError(
                    CONFLICTING_FILENAME_ERROR.format(filename=marker.filename)
                )
            identifiers.add(identifier)
            filenames.add(marker.filename)
            markers.append(marker)
    if not markers:
        raise ValueError(NO_OBJECTS_ERROR)
    return markers


def load_settings(
    data: PrintConfiguration | Mapping[str, object],
    grid: tuple[int, int] | None,
) -> LabelSettings:
    """Resolve the selected sheet profile and validate print geometry.

    :param data: Print configuration model or decoded TOML.
    :param grid: Optional column and row override.
    :return: Validated print settings.
    :raises ValueError: If the supplied values are invalid.
    """
    configuration: PrintConfiguration
    if isinstance(data, PrintConfiguration):
        configuration = data
    elif set(data).issubset(PrintConfiguration.model_fields):
        configuration = PrintConfiguration.model_validate(data)
    else:
        configuration = MarkerConfig.model_validate(data)
    config: LabelsConfig = configuration.labels
    layout: Layout
    if config.profile == LabelProfile.AVERY_L7160:
        layout = AVERY_L7160
    elif config.profile == LabelProfile.CUSTOM:
        if config.custom is None:
            raise ValueError(CUSTOM_LAYOUT_REQUIRED)
        layout = config.custom
    else:
        grid_config: GridConfig = config.grid
        columns: int
        rows: int
        columns, rows = grid or (grid_config.columns, grid_config.rows)
        if columns < 1 or rows < 1:
            raise ValueError(GRID_DIMENSIONS_ERROR)
        layout = Layout(
            page_width_mm=grid_config.page_width_mm,
            page_height_mm=grid_config.page_height_mm,
            columns=columns,
            rows=rows,
            label_width_mm=(
                grid_config.page_width_mm
                - PADDING_SIDES * grid_config.margin_x_mm
                - (columns - 1) * grid_config.gap_x_mm
            )
            / columns,
            label_height_mm=(
                grid_config.page_height_mm
                - PADDING_SIDES * grid_config.margin_y_mm
                - (rows - 1) * grid_config.gap_y_mm
            )
            / rows,
            margin_left_mm=grid_config.margin_x_mm,
            margin_top_mm=grid_config.margin_y_mm,
            gap_x_mm=grid_config.gap_x_mm,
            gap_y_mm=grid_config.gap_y_mm,
        )
    if grid is not None and config.profile != LabelProfile.A4_GRID:
        layout = Layout.model_validate(
            dict(layout.model_dump(), columns=grid[0], rows=grid[1])
        )
    return LabelSettings(
        layout=layout,
        qr_size_mm=config.qr_size_mm,
        padding_mm=config.padding_mm,
        start_index=config.start_index,
        show_text=config.show_text,
        draw_guides=config.draw_guides,
        shift_x_mm=config.shift_x_mm,
        shift_y_mm=config.shift_y_mm,
    )
