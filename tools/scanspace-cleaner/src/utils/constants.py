"""Name CLI arguments, ScanSpace fields and geometry identifiers."""

from typing import Final, Literal

CLEAN: Final[Literal["clean"]] = "clean"
SCANSPACE: Final[str] = "scanspace"
CONFIG_OPTION: Final[str] = "--config"
READ_BINARY_MODE: Final[str] = "rb"
FIRST_WINDOW_INDEX: Final[int] = 1
TRANSFORM_SIDE: Final[int] = 4
TRANSFORM_ELEMENTS: Final[int] = TRANSFORM_SIDE * TRANSFORM_SIDE
MAIN_MODULE: Final[Literal["__main__"]] = "__main__"
GLB_SUFFIX: Final[str] = ".glb"
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
