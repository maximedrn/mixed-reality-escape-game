"""Call the native FreeMoCap V2 posthoc pipeline as imported Python modules."""

from __future__ import annotations

from atexit import register
from functools import cache
from importlib import import_module
from multiprocessing import Value
from multiprocessing.sharedctypes import Synchronized
from pathlib import Path
from threading import Event, Thread
from time import monotonic, perf_counter, sleep
from types import ModuleType
from typing import TYPE_CHECKING, Any, Protocol, cast

from src.models.runtime import Batch, Job
from src.utils.constants import (
    ALL_FILES_GLOB,
    BINARY_FLAG_TYPE,
    CALIBRATION_FILE,
    FREEMOCAP_CONFIG_MODULE,
    FREEMOCAP_LOG_CONSUMER_MODULE,
    FREEMOCAP_MANAGER_MODULE,
    MIN_CAMERAS,
    MULTIPROCESSING_QUEUES_MODULE,
    OUTPUT_DATA_DIR,
    POLL_SECONDS,
    PROCESS_MODE,
    RESULT_EXTENSIONS,
    SKELLYCAM_INFO_MODULE,
    SKELLYCAM_MANAGED_MODULE,
    SKELLYCAM_WORKERS_MODULE,
    SKELLYLOGS_MODULE,
    STATUS_FAILED,
)
from src.utils.messages import (
    MISSING_FREEMOCAP,
    PROCESS_EXITED,
    PROCESS_FAILED,
    PROCESS_TIMED_OUT,
    PROGRESS,
)

if TYPE_CHECKING:
    from multiprocessing.queues import Queue


class ProgressMessage(Protocol):  # pylint: disable=too-few-public-methods
    """Fields read from a native FreeMoCap progress message."""

    pipeline_id: str
    phase: str
    progress_fraction: float
    detail: str


class Pipeline(Protocol):
    """Methods used to monitor and shut down the native pipeline."""

    @property
    def alive(self) -> bool:
        """Indicate whether the native pipeline is running.

        :return: Whether the native pipeline is running.
        :rtype: bool
        """
        ...

    def get_progress_messages(self) -> list[ProgressMessage]:
        """Collect messages from the running pipeline.

        :return: Messages available from the live pipeline.
        :rtype: list[ProgressMessage]
        """
        ...

    def drain_and_get_messages(self) -> list[ProgressMessage]:
        """Collect the remaining messages after exit.

        :return: Messages buffered during pipeline shutdown.
        :rtype: list[ProgressMessage]
        """
        ...

    def shutdown(self) -> None:
        """Close the native pipeline and release its workers.

        :return: No return value.
        :rtype: None
        """
        ...


@cache
def resolve_api() -> tuple[Any, Any, Any, Any, Any]:
    """Import posthoc classes from FreeMoCap V2 only when processing.

    :return: The five runtime classes from FreeMoCap and SkellyCam.
    :rtype: tuple[Any, Any, Any, Any, Any]
    """
    try:
        # SkellyCam references multiprocessing.queues.Queue at import time.
        # Python does not expose this submodule until explicitly imported.
        import_module(MULTIPROCESSING_QUEUES_MODULE)
        info: ModuleType = import_module(SKELLYCAM_INFO_MODULE)
        worker: ModuleType = import_module(SKELLYCAM_WORKERS_MODULE)
        managed: ModuleType = import_module(SKELLYCAM_MANAGED_MODULE)
        log_consumer: ModuleType = import_module(FREEMOCAP_LOG_CONSUMER_MODULE)
        skellylogs: ModuleType = import_module(SKELLYLOGS_MODULE)
        log_queue: Queue[dict[str, object]] = (
            skellylogs.get_websocket_log_queue()
        )
        # Headless runs have no frontend to flush after the consumer stops.
        log_queue.cancel_join_thread()
        log_consumer.start_log_queue_consumer()
        register(log_consumer.stop_log_queue_consumer)
        manager: ModuleType = import_module(FREEMOCAP_MANAGER_MODULE)
        config: ModuleType = import_module(FREEMOCAP_CONFIG_MODULE)
    except ImportError as error:
        raise RuntimeError(MISSING_FREEMOCAP) from error
    return (
        info.RecordingInfo,
        worker.WorkerRegistry,
        managed.WorkerMode,
        manager.PosthocPipelineManager,
        config.PosthocMocapPipelineConfig,
    )


def pulse_heartbeat(
    timestamp: Synchronized[float],
    stop_event: Event,
) -> None:
    """Keep FreeMoCap child workers informed of parent health.

    :param timestamp: Shared heartbeat timestamp from the SkellyCam registry.
    :type timestamp: Synchronized[float]
    :param stop_event: Flag set when native processing finishes.
    :type stop_event: Event
    :return: No return value.
    :rtype: None
    """
    while not stop_event.is_set():
        with timestamp.get_lock():
            timestamp.value = perf_counter()
        stop_event.wait(timeout=POLL_SECONDS)


def is_valid_output(folder: Path) -> bool:
    """Require usable 3D output before publishing a clip.

    :param folder: Temporary FreeMoCap recording directory.
    :type folder: Path
    :return: Whether the native output folder contains data files.
    :rtype: bool
    """
    data: Path = folder / OUTPUT_DATA_DIR
    return data.is_dir() and any(
        path.is_file()
        and path.stat().st_size > 0
        and path.suffix.lower() in RESULT_EXTENSIONS
        for path in data.rglob(ALL_FILES_GLOB)
    )


def process_recording(
    job: Job,
    batch: Batch,
    working_dir: Path,
    fps: float,
    timeout: float,
) -> None:
    """Process one synchronized multi-camera clip using FreeMoCap modules.

    :param job: Animation name and input camera videos.
    :type job: Job
    :param batch: Common tracker parameters and calibration location.
    :type batch: Batch
    :param working_dir: Temp staging folder containing recording manifest.
    :type working_dir: Path
    :param fps: Verified common source video frame rate.
    :type fps: float
    :param timeout: Max seconds allowed for this recording.
    :type timeout: float
    :return: No return value.
    :rtype: None
    """
    (
        recording_type,
        registry_type,
        worker_modes,
        manager_type,
        config_type,
    ) = resolve_api()
    flag: Synchronized[int] = Value(BINARY_FLAG_TYPE, False)
    registry: Any = registry_type(
        global_kill_flag=flag,
        worker_mode=getattr(worker_modes, PROCESS_MODE),
    )
    manager: Any = manager_type(
        global_kill_flag=flag, worker_registry=registry
    )
    stop_event: Event = Event()
    heartbeat: Thread = Thread(
        target=pulse_heartbeat,
        args=(registry.heartbeat_timestamp, stop_event),
        daemon=True,
    )
    heartbeat.start()
    pipeline: Pipeline | None = None
    try:
        recording: Any = recording_type(
            recording_name=working_dir.name,
            recording_directory=str(working_dir.parent),
        )
        config: Any = config_type(
            detector_type=batch.detector,
            rtmpose_model_name=batch.model_name,
            rtmpose_confidence_threshold=batch.confidence,
            video_fps=fps,
            calibration_toml_path=str(working_dir / CALIBRATION_FILE),
            export_to_blender=False,
            auto_open_blend_file=False,
        )
        pipeline = cast(
            Pipeline,
            manager.create_mocap_pipeline(
                recording_info=recording,
                mocap_config=config,
            ),
        )
        monitor_pipeline(pipeline, job.name, working_dir, timeout)
    finally:
        if pipeline is not None:
            pipeline.shutdown()
        manager.shutdown()
        stop_event.set()
        heartbeat.join(timeout=POLL_SECONDS * MIN_CAMERAS)
        registry.shutdown_all()


def monitor_pipeline(
    pipeline: Pipeline,
    name: str,
    working_dir: Path,
    timeout: float,
) -> None:
    """Track native progress and reject unsuccessful jobs.

    :param pipeline: Started FreeMoCap native posthoc pipeline.
    :type pipeline: Pipeline
    :param name: Animation name.
    :type name: str
    :param working_dir: Directory FreeMoCap must write results into.
    :type working_dir: Path
    :param timeout: Maximum runtime in seconds.
    :type timeout: float
    :return: No return value.
    :rtype: None
    """
    deadline: float = monotonic() + timeout
    last: dict[str, tuple[str, float]] = {}
    errors: list[str] = []
    while pipeline.alive:
        if monotonic() >= deadline:
            raise TimeoutError(PROCESS_TIMED_OUT.format(name=name))
        track_progress(pipeline.get_progress_messages(), name, last, errors)
        if errors:
            raise RuntimeError(
                PROCESS_FAILED.format(name=name, detail=errors[-1])
            )
        sleep(POLL_SECONDS)
    track_progress(pipeline.drain_and_get_messages(), name, last, errors)
    if errors:
        raise RuntimeError(PROCESS_FAILED.format(name=name, detail=errors[-1]))
    if not is_valid_output(working_dir):
        raise RuntimeError(PROCESS_EXITED.format(name=name))


def track_progress(
    messages: list[ProgressMessage],
    name: str,
    last: dict[str, tuple[str, float]],
    errors: list[str],
) -> None:
    """Deduplicate progress events and retain error messages.

    :param messages: Native FreeMoCap progress data.
    :type messages: list[ProgressMessage]
    :param name: Animation label for the CLI.
    :type name: str
    :param last: Last phase/fraction for each child process.
    :type last: dict[str, tuple[str, float]]
    :param errors: Accumulated failed progress events.
    :type errors: list[str]
    :return: No return value.
    :rtype: None
    """
    for message in messages:
        phase: str = str(message.phase).lower()
        progress: float = float(message.progress_fraction)
        child_id: str = str(message.pipeline_id)
        key: tuple[str, float] = (phase, round(progress, 2))
        if last.get(child_id) == key:
            continue
        last[child_id] = key
        detail: str = str(message.detail)
        if phase == STATUS_FAILED:
            errors.append(detail)
        print(
            PROGRESS.format(
                name=name,
                phase=phase,
                percent=progress * 100,
                detail=detail,
            ),
            flush=True,
        )
