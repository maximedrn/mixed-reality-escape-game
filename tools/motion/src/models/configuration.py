"""Read the typed project configuration."""

from pathlib import Path

from pydantic import Field

from src.config.defaults import (
    DEFAULT_GLB,
    DEFAULT_MODEL,
    DEFAULT_MOTION,
)
from src.models.base import FrozenModel


class InputConfig(FrozenModel):
    """Base rig and motion data paths."""

    model: Path = DEFAULT_MODEL
    animation: Path = DEFAULT_MOTION


class OutputConfig(FrozenModel):
    """Generated outputs."""

    glb: Path = DEFAULT_GLB


class ProjectConfig(FrozenModel):
    """Complete project settings."""

    inputs: InputConfig = Field(default_factory=InputConfig)
    outputs: OutputConfig = Field(default_factory=OutputConfig)
