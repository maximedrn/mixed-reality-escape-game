"""Create isolated FreeMoCap recordings and publish verified batch outputs."""

from __future__ import annotations

from json import dumps
from pathlib import Path
from shutil import copy2, rmtree
from tempfile import TemporaryDirectory

from tomlkit import dumps as toml_dumps
from tomlkit import parse
from tomlkit.toml_document import TOMLDocument

from src.models.runtime import Batch, Job, JobResult
from src.services.freemocap import process_recording
from src.services.validation import (
    calibration_camera_ids,
    read_calibration,
    validate_batch,
    validate_video_streams,
)
from src.utils.constants import (
    CALIBRATION_FILE,
    EMPTY_DETAILS,
    JSON_INDENT,
    JSON_MODEL_MODE,
    RECORDING_INFO_SUFFIX,
    REPORT_CALIBRATION_FIELD,
    REPORT_FILE,
    REPORT_RESULTS_FIELD,
    STATUS_FAILED,
    STATUS_SUCCESS,
    TEMP_PREFIX,
    TEMP_SUFFIX,
    UTF8_ENCODING,
    VIDEO_DIR,
    VIDEOS_FIELD,
)
from src.utils.messages import COMPLETED, EXISTS, STARTING


def stage_recording(
    job: Job,
    folder: Path,
    calibration: Path,
) -> None:
    """Create the FreeMoCap recording layout and explicit camera map.

    :param job: One animation and its camera inputs.
    :type job: Job
    :param folder: Staging directory to receive native 3D outputs.
    :type folder: Path
    :param calibration: Shared calibration TOML.
    :type calibration: Path
    :return: No return value.
    :rtype: None
    """
    video_dir: Path = folder / VIDEO_DIR
    video_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}
    for video in job.videos:
        filename: str = video.camera + video.path.suffix.lower()
        link: Path = video_dir / filename
        try:
            link.symlink_to(video.path)
        except (OSError, NotImplementedError):
            copy2(video.path, link)
        manifest[video.camera] = filename
    (folder / (folder.name + RECORDING_INFO_SUFFIX)).write_text(
        dumps({VIDEOS_FIELD: manifest}, indent=JSON_INDENT),
        encoding=UTF8_ENCODING,
    )
    full_calibration: dict[str, object] = read_calibration(calibration)
    camera_ids: list[str] = calibration_camera_ids(full_calibration)
    selected: set[str] = {video.camera for video in job.videos}
    document: TOMLDocument = parse(
        calibration.read_text(encoding=UTF8_ENCODING)
    )
    for camera in camera_ids:
        if camera not in selected:
            del document[camera]
    (folder / CALIBRATION_FILE).write_text(
        toml_dumps(document), encoding=UTF8_ENCODING
    )


def publish_recording(
    staging: Path,
    destination: Path,
    overwrite: bool,
) -> None:
    """Publish completed outputs only after native processing succeeds.

    :param staging: Complete staged FreeMoCap recording folder.
    :type staging: Path
    :param destination: Per-animation output folder.
    :type destination: Path
    :param overwrite: Whether an existing result may be replaced.
    :type overwrite: bool
    :return: No return value.
    :rtype: None
    """
    if destination.exists():
        if not overwrite:
            raise FileExistsError(EXISTS.format(path=destination))
        rmtree(destination)
    staging.replace(destination)


def run_one(
    job: Job,
    batch: Batch,
    calibration_sections: dict[str, object],
    overwrite: bool,
    timeout: float,
) -> JobResult:
    """Validate videos, process a recording, and publish its artifacts.

    :param job: Selected animation.
    :type job: Job
    :param batch: Shared capture settings.
    :type batch: Batch
    :param calibration_sections: Camera calibration data.
    :type calibration_sections: dict[str, object]
    :param overwrite: Allow replacement of already produced outputs.
    :type overwrite: bool
    :param timeout: Maximum processing time in seconds.
    :type timeout: float
    :return: One verified result status.
    :rtype: JobResult
    """
    destination: Path = batch.output / job.name
    if destination.exists() and not overwrite:
        raise FileExistsError(EXISTS.format(path=destination))
    fps: float = validate_video_streams(job, calibration_sections)
    with TemporaryDirectory(
        prefix=TEMP_PREFIX + job.name + TEMP_SUFFIX,
        dir=batch.output,
    ) as temp:
        working: Path = Path(temp) / job.name
        working.mkdir()
        stage_recording(job, working, batch.calibration)
        process_recording(job, batch, working, fps, timeout)
        publish_recording(working, destination, overwrite)
    print(COMPLETED.format(name=job.name, output=destination))
    return JobResult(
        name=job.name,
        status=STATUS_SUCCESS,
        directory=destination,
        details=EMPTY_DETAILS,
    )


def write_report(batch: Batch, results: list[JobResult]) -> None:
    """Write an audit trail of successful and failed animation jobs.

    :param batch: Common output path and calibration input.
    :type batch: Batch
    :param results: Per-animation processing results.
    :type results: list[JobResult]
    :return: No return value.
    :rtype: None
    """
    with TemporaryDirectory(dir=batch.output) as temp:
        report: Path = Path(temp) / REPORT_FILE
        report.write_text(
            dumps(
                {
                    REPORT_CALIBRATION_FIELD: str(batch.calibration),
                    REPORT_RESULTS_FIELD: [
                        result.model_dump(mode=JSON_MODEL_MODE)
                        for result in results
                    ],
                },
                indent=JSON_INDENT,
            ),
            encoding=UTF8_ENCODING,
        )
        report.replace(batch.output / REPORT_FILE)


def run_batch(batch: Batch) -> list[JobResult]:
    """Process configured animations sequentially and isolate failures.

    :param batch: Validated TOML configuration.
    :type batch: Batch
    :return: Result status for every attempted animation.
    :rtype: list[JobResult]
    """
    calib: dict[str, object] = validate_batch(batch)
    if batch.jobs and not batch.processing.overwrite:
        first: Path = batch.output / batch.jobs[0].name
        if first.exists() and (
            not batch.processing.continue_on_error
            or all((batch.output / job.name).exists() for job in batch.jobs)
        ):
            raise FileExistsError(EXISTS.format(path=first))
    batch.output.mkdir(parents=True, exist_ok=True)
    results: list[JobResult] = []
    for index, job in enumerate(batch.jobs, start=1):
        print(
            STARTING.format(
                index=index,
                total=len(batch.jobs),
                name=job.name,
                cameras=len(job.videos),
            )
        )
        result: JobResult
        try:
            result = run_one(
                job,
                batch,
                calib,
                batch.processing.overwrite,
                batch.processing.timeout_seconds,
            )
        except (OSError, RuntimeError, ValueError, TimeoutError) as error:
            result = JobResult(
                name=job.name,
                status=STATUS_FAILED,
                directory=batch.output / job.name,
                details=str(error),
            )
            results.append(result)
            write_report(batch, results)
            if not batch.processing.continue_on_error:
                raise
        else:
            results.append(result)
            write_report(batch, results)
    return results
