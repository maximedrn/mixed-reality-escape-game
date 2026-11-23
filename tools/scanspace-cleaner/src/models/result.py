"""Describe a completed architecture-only export."""

from pathlib import Path

from src.models.base import FrozenModel


class CleanResult(FrozenModel):
    """Store the output path and geometry counts of one cleaning pass."""

    output: Path
    original_faces: int
    clean_faces: int
    windows_filled: int
    bounds: list[list[float]]
    geometry: dict[str, int]
