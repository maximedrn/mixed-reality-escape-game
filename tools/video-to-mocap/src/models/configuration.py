"""Typed TOML configuration for recordings and processing."""

from __future__ import annotations

from typing import Self

from pydantic import Field, field_validator, model_validator

from src.models.base import FrozenModel
from src.utils.constants import (
    CLIP_PATTERN,
    DETECTOR_FIELD,
    MIN_CAMERAS,
    RTMPOSE_DETECTOR,
    VIDEOS_FIELD,
)
from src.utils.messages import (
    DUPLICATE_NAME,
    EMPTY_VIDEO_PATH,
    INVALID_DETECTOR,
)


class Animation(FrozenModel):
    """Define synchronized video paths in calibration-camera order."""

    name: str = Field(pattern=CLIP_PATTERN)
    videos: list[str] = Field(min_length=MIN_CAMERAS)

    @field_validator(VIDEOS_FIELD)
    @classmethod
    def verify_paths(cls, values: list[str]) -> list[str]:
        """Reject blank input paths.

        :param values: Configured video paths.
        :type values: list[str]
        :return: Validated paths.
        :rtype: list[str]
        """
        if any(not value.strip() for value in values):
            raise ValueError(EMPTY_VIDEO_PATH)
        return values


class CaptureConfig(FrozenModel):
    """Define a shared calibration file and tracker preferences."""

    calibration: str = Field(min_length=1)
    detector: str
    rtmpose_model_name: str = Field(min_length=1)
    confidence_threshold: float = Field(ge=0, le=1)

    @field_validator(DETECTOR_FIELD)
    @classmethod
    def verify_detector(cls, value: str) -> str:
        """Require the tested RTMPose posthoc path.

        :param value: Detector name from TOML.
        :type value: str
        :return: Accepted detector name.
        :rtype: str
        """
        if value != RTMPOSE_DETECTOR:
            raise ValueError(INVALID_DETECTOR.format(detector=value))
        return value


class OutputConfig(FrozenModel):
    """Configure the destination for independent FreeMoCap recordings."""

    directory: str = Field(min_length=1)


class ProcessingConfig(FrozenModel):
    """Configure time limits, output replacement and error handling."""

    timeout_seconds: float = Field(gt=0, allow_inf_nan=False)
    overwrite: bool = Field(strict=True)
    continue_on_error: bool = Field(strict=True)


class BatchConfig(FrozenModel):
    """Describe the complete multi-animation batch."""

    capture: CaptureConfig
    output: OutputConfig
    processing: ProcessingConfig
    animations: list[Animation] = Field(min_length=1)
    only: list[str] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def verify_names(self: Self) -> Self:
        """Require one unique output subdirectory per animation.

        :return: The validated batch configuration.
        :rtype: Self
        """
        names: set[str] = set()
        for animation in self.animations:
            if animation.name in names:
                raise ValueError(DUPLICATE_NAME.format(name=animation.name))
            names.add(animation.name)
        return self
