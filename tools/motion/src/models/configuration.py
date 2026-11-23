"""Read the typed project configuration."""

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import Field, model_validator

from src.models.base import FrozenModel
from src.models.motion import MAX_FPS
from src.utils.constants import GLB_FORMAT
from src.utils.messages import DUPLICATE_ANIMATION_NAMES_ERROR


class InputConfig(FrozenModel):
    """Base rig and motion data paths."""

    model: Path
    animation: Path | None = None
    constraints: Path | None = None


class OutputFormat(StrEnum):
    """Identify the supported animation container."""

    GLB = GLB_FORMAT  # noqa: TYP001, RUF100


class OutputConfig(FrozenModel):
    """Generated outputs."""

    glb: Path | None = None
    format: OutputFormat


class AnimationConfig(FrozenModel):
    """Describe one named input clip and its GLB destination."""

    name: str = Field(min_length=1)
    input: Path
    output: Path


class ProjectConfig(FrozenModel):
    """Complete project settings."""

    inputs: InputConfig
    outputs: OutputConfig
    animations: list[AnimationConfig] | None = None

    @model_validator(mode="after")
    def validate_names(self) -> Self:
        """Reject ambiguous animation names before any export.

        :return: The validated project configuration.
        :rtype: Self
        """
        names: list[str] = [
            animation.name for animation in self.animations or []
        ]
        if len(names) != len(set(names)):
            raise ValueError(DUPLICATE_ANIMATION_NAMES_ERROR)
        return self


class ExportConfig(FrozenModel):
    """Select an animated GLB, its source rig and JSON export settings."""

    input: Path
    model: Path
    output: Path
    fps: int = Field(gt=0, le=MAX_FPS)


class ValidateConfig(FrozenModel):
    """Select a motion JSON file to validate."""

    animation: Path
