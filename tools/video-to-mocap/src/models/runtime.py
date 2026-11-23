"""Validated job specifications and results independent of FreeMoCap."""

from __future__ import annotations

from pathlib import Path

from src.models.base import FrozenModel
from src.models.configuration import ProcessingConfig


class SourceVideo(FrozenModel):
    """Represent one resolved camera input."""

    camera: str
    path: Path


class Job(FrozenModel):
    """Represent one animation with its synchronized views."""

    name: str
    videos: list[SourceVideo]


class Batch(FrozenModel):
    """Carry resolved paths and processing settings for a batch."""

    calibration: Path
    output: Path
    detector: str
    model_name: str
    confidence: float
    processing: ProcessingConfig
    jobs: list[Job]


class JobResult(FrozenModel):
    """Report the final status of an animation job."""

    name: str
    status: str
    directory: Path
    details: str
