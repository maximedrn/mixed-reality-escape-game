"""Define generic filesystem defaults without a bundled character profile."""

from pathlib import Path
from typing import Final

PROJECT_CONFIG: Final[Path] = Path("assets/motion/config.toml")
DEFAULT_CONFIG: Final[Path] = next(
    (
        directory / PROJECT_CONFIG
        for directory in Path(__file__).resolve().parents
        if (directory / PROJECT_CONFIG).is_file()
    ),
    Path("config.toml"),
)
DEFAULT_MODEL: Final[Path] = Path("inputs/rig.glb")
DEFAULT_MOTION: Final[Path] = Path("inputs/motion.json")
DEFAULT_GLB: Final[Path] = Path("exports/motion.glb")
