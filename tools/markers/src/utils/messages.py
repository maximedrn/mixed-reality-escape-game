"""Centralize command-line descriptions and output messages."""

from typing import Final

CLI_DESCRIPTION: Final[str] = (
    "Generate vector QR markers and printable adhesive-label sheets."
)
CLI_CONFIG_HELP: Final[str] = (
    "TOML configuration (default: assets/markers/config.toml in the checkout, "
    "or ./config.toml for a standalone installation)."
)
CLI_OUTPUT_HELP: Final[str] = "Override the export directory."
CLI_GRID_HELP: Final[str] = "Override the label grid, for example 3x7."
GENERATED_MESSAGE: Final[str] = (
    "Generated {count} SVG markers and {destination}"
)
CUSTOM_LAYOUT_REQUIRED: Final[str] = (
    "The custom profile requires labels.custom"
)
NO_OBJECTS_ERROR: Final[str] = "No objects provided in config"
GRID_DIMENSIONS_ERROR: Final[str] = (
    "The grid must have positive columns and rows"
)
PAGE_DIMENSIONS_ERROR: Final[str] = (
    "Page and label dimensions must be positive"
)
PAGE_SPACING_ERROR: Final[str] = "Margins and gaps must be non-negative"
PAGE_WIDTH_ERROR: Final[str] = "Label grid exceeds page width"
PAGE_HEIGHT_ERROR: Final[str] = "Label grid exceeds page height"
QR_DIMENSIONS_ERROR: Final[str] = (
    "QR size must be positive; padding non-negative"
)
QR_FIT_ERROR: Final[str] = "QR size and padding exceed label dimensions"
START_INDEX_ERROR: Final[str] = "start_index must fit on the first page"
PRINTER_OFFSETS_ERROR: Final[str] = (
    "Printer offsets move labels outside the page"
)
SVG_SIZE_ERROR: Final[str] = "SVG size must be positive"
SVG_PAYLOAD_ERROR: Final[str] = "SVG marker payload must not be empty"
GRID_ERROR: Final[str] = "Expected COLSxROWS (e.g. 3x7)"
IDENTIFIER_ERROR: Final[str] = (
    "Invalid {field} {value!r}: use lowercase letters, digits, "
    "underscores or hyphens"
)
DUPLICATE_MARKER_ERROR: Final[str] = "Duplicate marker: {payload}"
CONFLICTING_FILENAME_ERROR: Final[str] = "Conflicting SVG filename: {filename}"
