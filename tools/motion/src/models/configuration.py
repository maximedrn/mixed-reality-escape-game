"""Read the typed project configuration."""

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import Field, model_validator

from src.config.defaults import (
    DEFAULT_GLB,
    DEFAULT_MODEL,
    DEFAULT_MOTION,
)
from src.models.base import FrozenModel
from src.utils.constants import GLB_FORMAT
from src.utils.messages import DUPLICATE_ANIMATION_NAMES_ERROR


class InputConfig(FrozenModel):
    """Base rig and motion data paths."""

    model: Path = DEFAULT_MODEL
    animation: Path = DEFAULT_MOTION
    constraints: Path | None = None


class OutputFormat(StrEnum):
    """Identify the supported animation container."""

    GLB = GLB_FORMAT  # noqa: TYP001, RUF100


class OutputConfig(FrozenModel):
    """Generated outputs."""

    glb: Path = DEFAULT_GLB
    format: OutputFormat = OutputFormat.GLB


class AnimationConfig(FrozenModel):
    """Describe one named input clip and its GLB destination."""

    name: str = Field(min_length=1)
    input: Path
    output: Path


class ProjectConfig(FrozenModel):
    """Complete project settings."""

    inputs: InputConfig = Field(default_factory=InputConfig)
    outputs: OutputConfig = Field(default_factory=OutputConfig)
    animations: list[AnimationConfig] = Field(
        default_factory=list[AnimationConfig]
    )

    @model_validator(mode="after")
    def validate_names(self) -> Self:
        """Reject ambiguous animation names before any export.

        :return: The validated project configuration.
        :rtype: Self
        """
        names: list[str] = [animation.name for animation in self.animations]
        if len(names) != len(set(names)):
            raise ValueError(DUPLICATE_ANIMATION_NAMES_ERROR)
        return self
