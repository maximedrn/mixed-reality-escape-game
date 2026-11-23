"""Validate the ScanSpace TOML configuration."""

from pathlib import Path

from pydantic import Field

from src.models.base import FrozenModel


class CleanConfig(FrozenModel):
    """Select the matching source files and the cleaned GLB destination."""

    input: Path
    scan: Path
    output: Path
    window_overlap_m: float = Field(ge=0)
    window_depth_m: float = Field(gt=0)
