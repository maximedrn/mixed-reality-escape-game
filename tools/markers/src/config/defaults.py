"""Name standard paper dimensions and default print measurements."""

from pathlib import Path
from typing import Final

A4_WIDTH_MM: Final[float] = 210.0
A4_HEIGHT_MM: Final[float] = 297.0
AVERY_LABEL_WIDTH_MM: Final[float] = 63.5
AVERY_LABEL_HEIGHT_MM: Final[float] = 38.1
AVERY_MARGIN_LEFT_MM: Final[float] = 7.25
AVERY_MARGIN_TOP_MM: Final[float] = 15.15
AVERY_GAP_X_MM: Final[float] = 2.5
DEFAULT_GRID_MARGIN_MM: Final[float] = 10.0
DEFAULT_GRID_GAP_MM: Final[float] = 2.0
DEFAULT_QR_SIZE_MM: Final[float] = 30.0
DEFAULT_PADDING_MM: Final[float] = 2.0
PROJECT_CONFIG_PATH: Final[Path] = Path("assets/markers/config.toml")
DEFAULT_CONFIG_PATH: Final[Path] = next(
    (
        directory / PROJECT_CONFIG_PATH
        for directory in Path(__file__).resolve().parents
        if (directory / PROJECT_CONFIG_PATH).is_file()
    ),
    Path("config.toml"),
)
DEFAULT_OUTPUT_DIRECTORY: Final[str] = "exports"
