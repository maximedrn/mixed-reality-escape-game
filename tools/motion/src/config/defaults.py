"""Define generic filesystem defaults without a bundled character profile."""

from pathlib import Path
from typing import Final

DEFAULT_CONFIG: Final[Path] = Path("config.toml")
DEFAULT_MODEL: Final[Path] = Path("inputs/rig.glb")
DEFAULT_MOTION: Final[Path] = Path("inputs/motion.json")
DEFAULT_GLB: Final[Path] = Path("exports/motion.glb")
