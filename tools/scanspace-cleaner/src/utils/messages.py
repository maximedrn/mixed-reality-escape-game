"""Centralize CLI help, successful results and validation errors."""

from typing import Final

CLI_DESCRIPTION: Final[str] = (
    "Preserve ScanSpace walls, floor and doors, and fill window openings."
)
CLEAN_HELP: Final[str] = "Create an architecture-only ScanSpace GLB"
CONFIG_HELP: Final[str] = "TOML configuration file."
OUTPUT_MESSAGE: Final[str] = "Output: {output}"
ORIGINAL_FACES_MESSAGE: Final[str] = "Original faces: {count}"
CLEANED_FACES_MESSAGE: Final[str] = "Clean faces: {count}"
WINDOWS_MESSAGE: Final[str] = "Filled windows: {count}"
BOUNDS_MESSAGE: Final[str] = "Bounds: {bounds}"
GEOMETRY_MESSAGE: Final[str] = "Geometry: {geometry}"
OUTPUT_SUFFIX_ERROR: Final[str] = (
    "Output destination must have the .glb extension"
)
OUTPUT_OVERLAPS_INPUT_ERROR: Final[str] = (
    "Output destination cannot overwrite the configuration or an input file"
)
INVALID_MESH_ERROR: Final[str] = (
    "Missing or invalid triangular ScanSpace mesh: {name}"
)
MATERIAL_REQUIRED_ERROR: Final[str] = (
    "ScanSpace wall mesh requires a texture material to fill windows"
)
INVALID_WINDOW_DIMENSIONS_ERROR: Final[str] = (
    "Window width and height must be positive"
)
