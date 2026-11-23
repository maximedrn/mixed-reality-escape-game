"""Resolve a TOML project relative to the configuration file."""

from __future__ import annotations

from os.path import abspath
from pathlib import Path
from tomllib import load

from src.models.configuration import BatchConfig
from src.models.runtime import Batch, Job, SourceVideo
from src.services.validation import calibration_camera_ids, read_calibration
from src.utils.constants import (
    ALLOWED_VIDEO_EXTENSIONS,
    BINARY_READ_MODE,
    REPORT_FILE,
)
from src.utils.messages import (
    DUPLICATE_VIDEO,
    INVALID_VIDEO,
    INVALID_VIDEO_FORMAT,
    NOT_FOUND,
    OUTPUT_OVERLAPS_INPUT,
    TOO_MANY_VIDEOS,
)


def resolve_path(root: Path, value: str | Path) -> Path:
    """Expand user paths and resolve relative values from the TOML location.

    :param root: Directory containing the configuration file.
    :type root: Path
    :param value: Configured path, absolute or relative.
    :type value: str | Path
    :return: Absolute normalized path.
    :rtype: Path
    """
    path: Path = Path(value).expanduser()
    return (root / path).resolve()


def validate_destinations(
    config: BatchConfig,
    config_path: Path,
    output: Path,
    requested: set[str],
) -> None:
    """Keep output publication away from every configured input.

    :param config: Parsed configuration, including unselected animations.
    :type config: BatchConfig
    :param config_path: TOML path as supplied, before resolving symlinks.
    :type config_path: Path
    :param output: Resolved output directory.
    :type output: Path
    :param requested: Names selected for processing.
    :type requested: set[str]
    :return: No return value.
    :rtype: None
    """
    root: Path = config_path.resolve().parent
    inputs: set[Path] = {
        config_path,
        root / Path(config.capture.calibration).expanduser(),
        *(
            root / Path(video).expanduser()
            for animation in config.animations
            for video in animation.videos
        ),
    }
    protected: list[Path] = sorted(
        {
            location
            for source in inputs
            for location in (Path(abspath(source)), source.resolve())
        }
    )
    destinations: set[Path] = {output / name for name in requested}
    destinations.add(output / REPORT_FILE)
    for destination in sorted(destinations):
        resolved: Path = destination.resolve()
        for source in protected:
            if source.is_relative_to(destination) or source.is_relative_to(
                resolved
            ):
                raise ValueError(
                    OUTPUT_OVERLAPS_INPUT.format(
                        output=destination, source=source
                    )
                )


def load_configuration(path: Path) -> Batch:
    """Load TOML and check all user-specified paths before processing.

    :param path: TOML configuration path.
    :type path: Path
    :return: Validated, absolute input and output paths.
    :rtype: Batch
    """
    config_path: Path = path.expanduser()
    with config_path.open(BINARY_READ_MODE) as stream:
        config: BatchConfig = BatchConfig.model_validate(load(stream))
    root: Path = config_path.resolve().parent
    calibration: Path = resolve_path(root, config.capture.calibration)
    output: Path = resolve_path(root, config.output.directory)
    if not calibration.is_file():
        raise FileNotFoundError(INVALID_VIDEO.format(path=calibration))
    camera_ids: list[str] = calibration_camera_ids(
        read_calibration(calibration)
    )
    jobs: list[Job] = []
    defined: set[str] = {item.name for item in config.animations}
    requested: set[str] = defined if config.only is None else set(config.only)
    missing: set[str] = requested - defined
    if missing:
        raise ValueError(NOT_FOUND.format(names=sorted(missing)))
    validate_destinations(config, config_path, output, requested)
    for item in config.animations:
        if item.name not in requested:
            continue
        if len(item.videos) > len(camera_ids):
            raise ValueError(
                TOO_MANY_VIDEOS.format(
                    name=item.name,
                    videos=len(item.videos),
                    cameras=len(camera_ids),
                )
            )
        videos: list[SourceVideo] = []
        seen: set[Path] = set()
        for camera, video_path in zip(camera_ids, item.videos, strict=False):
            source: Path = resolve_path(root, video_path)
            if not source.is_file():
                raise FileNotFoundError(INVALID_VIDEO.format(path=source))
            if source.suffix.lower() not in ALLOWED_VIDEO_EXTENSIONS:
                raise ValueError(INVALID_VIDEO_FORMAT.format(path=source))
            if source in seen:
                raise ValueError(DUPLICATE_VIDEO.format(path=source))
            seen.add(source)
            videos.append(SourceVideo(camera=camera, path=source))
        jobs.append(Job(name=item.name, videos=videos))
    return Batch(
        calibration=calibration,
        output=output,
        detector=config.capture.detector,
        model_name=config.capture.rtmpose_model_name,
        confidence=config.capture.confidence_threshold,
        processing=config.processing,
        jobs=jobs,
    )
