"""Validate command-specific arguments at the CLI boundary."""

from enum import StrEnum
from pathlib import Path

from pydantic import Field, FilePath

from src.models.base import FrozenModel
from src.models.motion import MAX_FPS
from src.utils.constants import (
    BUILD,
    EXPORT_JSON,
    VALIDATE,
)


class Command(StrEnum):
    """Name the supported motion operations."""

    BUILD = BUILD  # noqa: TYP001, RUF100
    EXPORT_JSON = EXPORT_JSON  # noqa: TYP001, RUF100
    VALIDATE = VALIDATE  # noqa: TYP001, RUF100


class CommandArguments(FrozenModel):
    """Identify the requested operation."""

    command: Command


class BuildArguments(CommandArguments):
    """Select configuration paths and optional build overrides."""

    config: Path
    model: Path | None = None
    animation: Path | None = None
    output: Path | None = None


class ExportArguments(CommandArguments):
    """Select the input rig, animated GLB and output JSON."""

    input: FilePath
    model: FilePath
    output: Path
    fps: int = Field(gt=0, le=MAX_FPS)


class ValidateArguments(CommandArguments):
    """Select a motion JSON to validate."""

    animation: FilePath
