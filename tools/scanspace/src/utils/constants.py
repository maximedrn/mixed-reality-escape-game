"""Name CLI arguments, ScanSpace fields and geometry identifiers."""

from typing import Final, Literal

CLEAN: Final[Literal["clean"]] = "clean"
SCANSPACE: Final[str] = "scanspace"
COMMAND_KEY: Final[Literal["command"]] = "command"
INPUT_OPTION: Final[str] = "--input"
SCAN_OPTION: Final[str] = "--scan"
OUTPUT_OPTION: Final[str] = "--output"
MAIN_MODULE: Final[Literal["__main__"]] = "__main__"
GLB_SUFFIX: Final[str] = ".glb"
SCENE_FORMAT: Final[Literal["scene"]] = "scene"
STRUCTURE_JSON_PATH: Final[str] = "room/structure.json"
DIMENSIONS_FIELD: Final[str] = "dimensions"
WINDOW_NAME_TEMPLATE: Final[str] = "FilledWindow_{index}"
WALL_GEOMETRY_NAME: Final[str] = "Room"
FLOOR_GEOMETRY_NAME: Final[str] = "Room_1"
DOOR_GEOMETRY_NAME: Final[str] = "Room_3"
WALL_OUTPUT_NAME: Final[str] = "Walls"
FLOOR_OUTPUT_NAME: Final[str] = "Floor"
DOOR_OUTPUT_NAME: Final[str] = "Doors"
ARCHITECTURE_MESHES: Final[tuple[tuple[str, str], ...]] = (
    (WALL_OUTPUT_NAME, WALL_GEOMETRY_NAME),
    (FLOOR_OUTPUT_NAME, FLOOR_GEOMETRY_NAME),
    (DOOR_OUTPUT_NAME, DOOR_GEOMETRY_NAME),
)
FORBID: Final[Literal["forbid"]] = "forbid"
IGNORE: Final[Literal["ignore"]] = "ignore"
