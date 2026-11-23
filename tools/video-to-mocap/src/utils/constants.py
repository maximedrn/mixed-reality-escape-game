"""Shared literal values and public command names."""

from typing import Final, Literal

APPLICATION: Final[str] = "freemocap-batch"
BUILD: Final[str] = "build"
VALIDATE: Final[str] = "validate"
CONFIG_OPTION: Final[str] = "--config"
COMMAND_KEY: Final[str] = "command"
CONFIG_FIELD: Final[str] = "config"
OUTPUT_FIELD: Final[str] = "output"
ONLY_FIELD: Final[str] = "only"
OVERWRITE_FIELD: Final[str] = "overwrite"
CONTINUE_FIELD: Final[str] = "continue_on_error"
TIMEOUT_FIELD: Final[str] = "timeout"
ANIMATION_FIELD: Final[str] = "animations"
CAMERA_FIELD: Final[str] = "camera"
PATH_FIELD: Final[str] = "path"
VIDEOS_FIELD: Final[str] = "videos"
VIDEO_DIR: Final[str] = "synchronized_videos"
OUTPUT_DATA_DIR: Final[str] = "output_data"
ALL_FILES_GLOB: Final[str] = "*"
RECORDING_INFO_SUFFIX: Final[str] = "_recording_info.json"
REPORT_FILE: Final[str] = "batch_report.json"
CALIBRATION_FILE: Final[str] = "camera_calibration.toml"
STATUS_FAILED: Final[str] = "failed"
STATUS_COMPLETE: Final[str] = "complete"
STATUS_SUCCESS: Final[str] = "success"
STATUS_SKIPPED: Final[str] = "skipped"
RESULT_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {".npy", ".parquet", ".csv"}
)
ALLOWED_VIDEO_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {".mp4", ".mov", ".mkv", ".avi"}
)
CLIP_PATTERN: Final[str] = r"^[a-z][a-z0-9_]*$"
FREEMOCAP_MODULE: Final[str] = "freemocap"
FREEMOCAP_MANAGER_MODULE: Final[str] = (
    "freemocap.core.pipeline.posthoc.posthoc_pipeline_manager"
)
FREEMOCAP_CONFIG_MODULE: Final[str] = (
    "freemocap.core.tasks.mocap.mocap_task_config"
)
FREEMOCAP_LOG_CONSUMER_MODULE: Final[str] = (
    "freemocap.system.logging.log_queue_consumer"
)
MULTIPROCESSING_QUEUES_MODULE: Final[str] = "multiprocessing.queues"
SKELLYCAM_INFO_MODULE: Final[str] = (
    "skellycam.core.recorders.videos.recording_info"
)
SKELLYCAM_WORKERS_MODULE: Final[str] = (
    "skellycam.core.ipc.process_management.worker_registry"
)
SKELLYCAM_MANAGED_MODULE: Final[str] = (
    "skellycam.core.ipc.process_management.managed_worker"
)
SKELLYLOGS_MODULE: Final[str] = "skellylogs"
CV2_MODULE: Final[str] = "cv2"
PROCESS_MODE: Final[str] = "PROCESS"
MIN_CAMERAS: Final[int] = 2
FPS_TOLERANCE: Final[float] = 0.15
FPS_ERROR_RATIO: Final[float] = 0.02
POLL_SECONDS: Final[float] = 0.5
POST_EXIT_DRAIN_SECONDS: Final[float] = 1.0
JSON_INDENT: Final[int] = 2

ENTRYPOINT_NAME: Final[str] = "__main__"
UTF8_ENCODING: Final[str] = "utf-8"
BINARY_READ_MODE: Final[str] = "rb"
BINARY_FLAG_TYPE: Final[str] = "b"
CALIBRATION_SIZE_FIELD: Final[str] = "size"
CALIBRATION_SIZE_DIMENSIONS: Final[int] = 2
REPORT_CALIBRATION_FIELD: Final[str] = "calibration"
REPORT_RESULTS_FIELD: Final[str] = "results"
JSON_MODEL_MODE: Final[str] = "json"
TEMP_PREFIX: Final[str] = "."
TEMP_SUFFIX: Final[str] = "_"
DETECTOR_FIELD: Final[str] = "detector"
RTMPOSE_DETECTOR: Final[str] = "rtmpose"
EMPTY_DETAILS: Final[str] = ""
EXTRA_FORBID: Final[Literal["forbid"]] = "forbid"
