"""Centralize user-visible messages and errors."""

from typing import Final

CLI_DESCRIPTION: Final[str] = (
    "Process multi-view clips with FreeMoCap's Python posthoc pipeline."
)
BUILD_HELP: Final[str] = "Process all configured clips sequentially."
VALIDATE_HELP: Final[str] = (
    "Check inputs and camera calibration without running FreeMoCap."
)
CONFIG_HELP: Final[str] = "Path to the TOML project configuration."
INVALID_DETECTOR: Final[str] = (
    "Unsupported detector: {detector}. Only RTMPose is supported."
)
INVALID_CALIBRATION: Final[str] = (
    "Calibration has no camera section for: {camera}"
)
INVALID_CAMERA_COUNT: Final[str] = (
    "Animation '{name}' needs at least two calibrated camera views."
)
INVALID_VIDEO: Final[str] = "Video file does not exist: {path}"
INVALID_VIDEO_FORMAT: Final[str] = "Unsupported video extension: {path}"
DUPLICATE_VIDEO: Final[str] = "A video is reused in the same animation: {path}"
EMPTY_VIDEO_PATH: Final[str] = "Video paths cannot be empty."
NO_CALIBRATED_CAMERAS: Final[str] = (
    "Calibration does not define any camera sections with size data."
)
CAMERA_ORDER_MISMATCH: Final[str] = (
    "Camera order for '{name}': got {actual}, expected {expected}."
)
TOO_MANY_VIDEOS: Final[str] = (
    "Animation '{name}' has {videos} videos, but calibration has only "
    "{cameras} cameras. Order videos as camera sections in calibration."
)
DUPLICATE_NAME: Final[str] = "Animation names must be unique: {name}"
NO_ANIMATIONS: Final[str] = (
    "The TOML must define at least one [[animations]] entry."
)
NOT_FOUND: Final[str] = "Unknown animation name(s): {names}"
MISSING_FREEMOCAP: Final[str] = (
    "FreeMoCap 2 module API is unavailable. Install the optional 'freemocap' "
    "extra or provide a compatible FreeMoCap 2 checkout."
)
EXISTS: Final[str] = (
    "Output already exists: {path} (set processing.overwrite = true)"
)
OUTPUT_OVERLAPS_INPUT: Final[str] = "Output {output} overlaps input {source}"
PROCESS_FAILED: Final[str] = "FreeMoCap failed for '{name}': {detail}"
PROCESS_EXITED: Final[str] = (
    "FreeMoCap exited without verified 3D output for '{name}'."
)
PROCESS_TIMED_OUT: Final[str] = (
    "FreeMoCap exceeded the per-animation timeout for '{name}'."
)
INVALID_VIDEO_STREAM: Final[str] = "Cannot read video metadata: {path}"
FRAMES_MISMATCH: Final[str] = (
    "Camera frame counts differ in animation '{name}': {counts}"
)
FPS_MISMATCH: Final[str] = (
    "Camera FPS values differ in animation '{name}': {fps}"
)
RESOLUTION_MISMATCH: Final[str] = (
    "Camera '{camera}' video is {actual} but calibration expects {expected}."
)
CALIBRATION_SIZE_MISSING: Final[str] = (
    "Calibration size is missing for camera '{camera}'."
)
STARTING: Final[str] = "Processing {index}/{total}: {name} ({cameras} cameras)"
COMPLETED: Final[str] = "Finished: {name} -> {output}"
VALIDATED: Final[str] = (
    "Validated {count} animation(s), calibration and video paths."
)
PROGRESS: Final[str] = "[{name}] {phase} {percent:.0f}% {detail}"
RESULT_SUMMARY: Final[str] = (
    "Batch completed: {success} succeeded, {failed} failed."
)

CAMERA_ASSIGNMENT: Final[str] = "{name}: {cameras}"
CAMERA_ASSIGNMENT_ITEM: Final[str] = "{camera} = {filename}"
CAMERA_ASSIGNMENT_SEPARATOR: Final[str] = ", "
