"""Validate the ScanSpace command-line arguments."""

from enum import StrEnum
from pathlib import Path

from pydantic import FilePath

from src.models.base import FrozenModel
from src.utils.constants import CLEAN


class Command(StrEnum):
    """Name the supported ScanSpace operations."""

    CLEAN = CLEAN  # noqa: TYP001, RUF100


class CleanArguments(FrozenModel):
    """Select the matching source files and the cleaned GLB destination."""

    command: Command
    input: FilePath
    scan: FilePath
    output: Path
