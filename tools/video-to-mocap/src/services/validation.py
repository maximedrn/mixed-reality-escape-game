"""Check calibration identifiers and video consistency."""

from __future__ import annotations

from importlib import import_module
from math import isfinite
from pathlib import Path
from tomllib import load
from typing import Any, cast

from src.models.runtime import Batch, Job
from src.utils.constants import (
    BINARY_READ_MODE,
    CALIBRATION_SIZE_DIMENSIONS,
    CALIBRATION_SIZE_FIELD,
    CV2_MODULE,
    FPS_ERROR_RATIO,
    FPS_TOLERANCE,
    MIN_CAMERAS,
)
from src.utils.messages import (
    CALIBRATION_SIZE_MISSING,
    CAMERA_ORDER_MISMATCH,
    FPS_MISMATCH,
    FRAMES_MISMATCH,
    INVALID_CAMERA_COUNT,
    INVALID_VIDEO_STREAM,
    NO_CALIBRATED_CAMERAS,
    RESOLUTION_MISMATCH,
    TOO_MANY_VIDEOS,
)


def read_calibration(path: Path) -> dict[str, Any]:
    """Read a FreeMoCap calibration file without modifying it.

    :param path: Calibration TOML path.
    :type path: Path
    :return: Parsed calibration sections.
    :rtype: dict[str, Any]
    """
    with path.open(BINARY_READ_MODE) as stream:
        return load(stream)


def calibration_camera_ids(calibration: dict[str, Any]) -> list[str]:
    """Return calibrated camera IDs in original TOML section order.

    Ignore FreeMoCap metadata sections; only sections with a video size
    identify cameras. This preserves implicit video-to-camera mapping.

    :param calibration: Parsed FreeMoCap calibration.
    :type calibration: dict[str, Any]
    :return: Camera identifiers in file order.
    :rtype: list[str]
    """
    names: list[str] = [
        name
        for name, section in calibration.items()
        if isinstance(section, dict) and CALIBRATION_SIZE_FIELD in section
    ]
    if not names:
        raise ValueError(NO_CALIBRATED_CAMERAS)
    return names


def validate_batch(batch: Batch) -> dict[str, Any]:
    """Verify camera counts and calibration identifiers.

    :param batch: Absolute user configuration.
    :type batch: Batch
    :return: Parsed camera calibration.
    :rtype: dict[str, Any]
    """
    calib: dict[str, Any] = read_calibration(batch.calibration)
    camera_ids: list[str] = calibration_camera_ids(calib)
    for job in batch.jobs:
        if len(job.videos) < MIN_CAMERAS:
            raise ValueError(INVALID_CAMERA_COUNT.format(name=job.name))
        if len(job.videos) > len(camera_ids):
            raise ValueError(
                TOO_MANY_VIDEOS.format(
                    name=job.name,
                    videos=len(job.videos),
                    cameras=len(camera_ids),
                )
            )
        for index, video in enumerate(job.videos):
            if video.camera != camera_ids[index]:
                raise ValueError(
                    CAMERA_ORDER_MISMATCH.format(
                        name=job.name,
                        actual=video.camera,
                        expected=camera_ids[index],
                    )
                )
    return calib


def validate_video_streams(job: Job, calibration: dict[str, Any]) -> float:
    """Check frames, FPS and resolutions using FreeMoCap's OpenCV dependency.

    :param job: One animation recorded from two or more cameras.
    :type job: Job
    :param calibration: Camera calibration sections.
    :type calibration: dict[str, Any]
    :return: Common nominal frame rate.
    :rtype: float
    """
    cv2: Any = import_module(CV2_MODULE)
    counts: dict[str, int] = {}
    rates: dict[str, float] = {}
    for video in job.videos:
        reader: Any = cv2.VideoCapture(str(video.path))
        try:
            if not reader.isOpened():
                raise ValueError(INVALID_VIDEO_STREAM.format(path=video.path))
            count: int = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
            fps: float = float(reader.get(cv2.CAP_PROP_FPS))
            width: int = int(reader.get(cv2.CAP_PROP_FRAME_WIDTH))
            height: int = int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if count <= 0 or not isfinite(fps) or fps <= 0:
                raise ValueError(INVALID_VIDEO_STREAM.format(path=video.path))
            counts[video.camera] = count
            rates[video.camera] = fps
            size: object = calibration[video.camera].get(
                CALIBRATION_SIZE_FIELD
            )
            expected: list[object] = (
                cast(list[object], size) if isinstance(size, list) else []
            )
            if len(expected) != CALIBRATION_SIZE_DIMENSIONS:
                raise ValueError(
                    CALIBRATION_SIZE_MISSING.format(camera=video.camera)
                )
            if [width, height] != expected:
                raise ValueError(
                    RESOLUTION_MISMATCH.format(
                        camera=video.camera,
                        actual=[width, height],
                        expected=expected,
                    )
                )
        finally:
            reader.release()
    if len(set(counts.values())) != 1:
        raise ValueError(FRAMES_MISMATCH.format(name=job.name, counts=counts))
    fps_values: list[float] = list(rates.values())
    tolerance: float = max(FPS_TOLERANCE, min(fps_values) * FPS_ERROR_RATIO)
    if max(fps_values) - min(fps_values) > tolerance:
        raise ValueError(FPS_MISMATCH.format(name=job.name, fps=rates))
    return fps_values[0]
