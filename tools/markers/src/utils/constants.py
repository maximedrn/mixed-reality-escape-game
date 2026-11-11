"""Name shared file conventions and physical layout calculations."""

from typing import Final, Literal

TEXT_ENCODING: Final[str] = "utf-8"
READ_BINARY_MODE: Final[str] = "rb"
WRITE_TEXT_MODE: Final[str] = "w"
SVG_DIRECTORY: Final[str] = "svg"
PDF_FILENAME: Final[str] = "labels.pdf"
MANIFEST_FILENAME: Final[str] = "markers.csv"
GEOMETRY_EPSILON: Final[float] = 1e-7
PADDING_SIDES: Final[int] = 2
CENTER_DIVISOR: Final[int] = 2
MAIN_MODULE: Final[str] = "__main__"
EMPTY_TEXT: Final[str] = ""
SPACE: Final[str] = " "
FONT_NAME: Final[str] = "Helvetica"
BLACK_HEX: Final[str] = "#000000"
LIGHT_GRAY_HEX: Final[str] = "#aaaaaa"
ELLIPSIS: Final[str] = "..."
PDF_TITLE: Final[str] = "Tohannic - QR marker labels"
PDF_AUTHOR: Final[str] = "Tohannic: No Way Out"
CONFIG_OPTION: Final[str] = "--config"
OUTPUT_OPTION: Final[str] = "--output"
GRID_OPTION: Final[str] = "--grid"
GRID_METAVAR: Final[str] = "COLSxROWS"
FORBID: Final[Literal["forbid"]] = "forbid"
ALWAYS: Final[Literal["always"]] = "always"
GAME_ID_FIELD: Final[str] = "game_id"
ROOM_ID_FIELD: Final[str] = "room_id"
OBJECT_ID_FIELD: Final[str] = "object_id"
ROOM_CONFIG_ID_FIELD: Final[str] = "id"
ROOM_OBJECTS_FIELD: Final[str] = "objects"
AVERY_L7160_PROFILE: Final[str] = "avery_l7160"
CUSTOM_PROFILE: Final[str] = "custom"
A4_GRID_PROFILE: Final[str] = "a4_grid"
IDENTIFIER_PATTERN: Final[str] = r"[a-z0-9][a-z0-9_-]*\Z"
GRID_PATTERN: Final[str] = r"([1-9]\d*)[xX]([1-9]\d*)"
MANIFEST_COLUMNS: Final[tuple[str, ...]] = (
    GAME_ID_FIELD,
    ROOM_ID_FIELD,
    OBJECT_ID_FIELD,
    "payload",
    SVG_DIRECTORY,
)
MANIFEST_SVG_TEMPLATE: Final[str] = "{directory}/{filename}"
MARKER_PAYLOAD_TEMPLATE: Final[str] = "{game_id}:{room_id}:{object_id}"
MARKER_FILENAME_TEMPLATE: Final[str] = "{room_id}_{object_id}.svg"
SVG_PATH_SEGMENT_TEMPLATE: Final[str] = "M{x} {y}h{width}v1h-{width}z"
SVG_DOCUMENT_TEMPLATE: Final[str] = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="{size_mm:g}mm" height="{total_height_mm:g}mm" '
    'viewBox="0 0 {size_mm:g} {total_height_mm:g}">\n'
    "<title>{safe_payload}</title>\n"
    '<rect width="{size_mm:g}" height="{total_height_mm:g}" '
    'fill="#ffffff"/>\n'
    '<g transform="scale({scale:.12g})" '
    'shape-rendering="crispEdges">\n'
    '<path d="{segments}" fill="#000000"/>\n'
    "</g>\n"
    '<text x="{center_mm:g}" y="{baseline_mm:.6g}" '
    'font-size="{font_size_mm:.6g}" '
    'font-family="Helvetica,Arial,sans-serif" '
    'text-anchor="middle" fill="#000000">{safe_payload}</text>\n'
    "</svg>\n"
)
