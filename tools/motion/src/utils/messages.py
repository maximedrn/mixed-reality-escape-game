"""Centralize CLI text, export results and application error messages."""

from typing import Final

NODE_TRANSFORM_ERROR: Final[str] = (
    "Node matrix must contain a nonsingular TRS transform without shear"
)
ANIMATED_BASE_MODEL_ERROR: Final[str] = "Base model must be unanimated"
ANIMATED_BONE_NOT_FOUND_ERROR: Final[str] = "Animated bone not found: {name}"
ANIMATED_GLB_MESSAGE: Final[str] = "Animated GLB: {glb}"
ANIMATED_REST_POSE_ERROR: Final[str] = (
    "Animated file does not match the base rig's rest pose"
)
ANIMATION_LOOP_ERROR: Final[str] = (
    "Animation not cyclic: first/last rotations differ"
)
BUILD_DESTINATIONS_ERROR: Final[str] = (
    "Build destination must differ from all inputs"
)
OUTPUT_GLB_SUFFIX_ERROR: Final[str] = (
    "Output destination must use the GLB extension (.glb)"
)
OUTPUT_ANIMATION_CONTENT_ERROR: Final[str] = (
    "Output GLB animation is missing, invalid or differs from the "
    "requested motion"
)
CLIP_TIMING_ERROR: Final[str] = (
    "Clip duration is not aligned with requested FPS"
)
CLI_DESCRIPTION: Final[str] = (
    "Build humanoid animation from rig + FreeMoCap-like JSON."
)
DUPLICATE_MARKER_NAMES_ERROR: Final[str] = "Duplicate marker names"
DUPLICATE_RIG_JOINT_NAMES_ERROR: Final[str] = "Duplicate rig joint names"
DUPLICATE_ROTATION_CHANNELS_ERROR: Final[str] = "Duplicate rotation channels"
DUPLICATE_TRACKED_JOINTS_ERROR: Final[str] = "Duplicate tracked joints"
EMBEDDED_BUFFER_REQUIRED_ERROR: Final[str] = (
    "Only embedded single-buffer GLBs are supported"
)
EXPORT_JSON_HELP: Final[str] = "Convert an existing animated GLB to JSON"
FPS_RANGE_ERROR: Final[str] = "FPS must be positive"
FRAME_EXPECTED_MARKERS_ERROR: Final[str] = (
    "Frame {frame_number}: expected {marker_count} markers"
)
FRAME_EXPECTED_ROTATIONS_ERROR: Final[str] = (
    "Frame {frame_number}: expected {bone_count} rotations"
)
FRAME_NON_UNIT_QUATERNION_ERROR: Final[str] = (
    "Frame {frame_number}: non-unit quaternion"
)
GENERATE_ANIMATED_GLB_HELP: Final[str] = "Generate a verified animated GLB"
GLB_CHUNKS_REQUIRED_ERROR: Final[str] = "Expected both JSON and BIN GLB chunks"
GLB_SCENE_ROOTS_DIFFER_ERROR: Final[str] = "GLB scene roots differ"
HORIZONTAL_ROOT_OFFSET_ERROR: Final[str] = (
    "Unexpected static horizontal root offset"
)
INCONSISTENT_GROUND_OFFSET_ERROR: Final[str] = (
    "Inconsistent grounding offset between scene roots"
)
INPUT_ANIMATION_COUNT_ERROR: Final[str] = (
    "Provide a GLB containing exactly one animation"
)
INVALID_GLB_HEADER_ERROR: Final[str] = "Invalid glTF 2.0 GLB header"
INVALID_RIG_SIGNATURE_ERROR: Final[str] = "Invalid rig SHA-256 signature"
JSON_EXPORTED_MESSAGE: Final[str] = (
    "JSON: {output} — {frame_count} frames, {marker_count} markers, "
    "{bone_count} animated bones"
)
LOOP_ROTATIONS_ERROR: Final[str] = (
    "Loop endpoints have different joint rotations"
)
MARKER_JOINT_NOT_FOUND_ERROR: Final[str] = "Marker joint not found: {bone}"
MARKER_POSE_MISMATCH_ERROR: Final[str] = (
    "Marker/rig mismatch ({value:.1f} mm): edit rig rotations and markers"
    " together, or re-export the JSON"
)
MOTION_FRAME_COUNT_ERROR: Final[str] = (
    "Marker and rig pose frame counts differ"
)
MOTION_REST_POSE_ERROR: Final[str] = (
    "Motion was captured on a different rest skeleton"
)
MOTION_VALID_MESSAGE: Final[str] = (
    "Valid: {name}, {frame_count} frames, {fps} FPS"
)
MULTIPLE_NODE_PARENTS_ERROR: Final[str] = "glTF node has multiple parents"
NOT_A_GLB_FILE_ERROR: Final[str] = "Not a GLB file: {path}"
OUTPUT_ANIMATED_GLB_PATH_HELP: Final[str] = "Output animated GLB path"
OUTPUT_ANIMATION_COUNT_ERROR: Final[str] = (
    "Output GLB does not contain exactly one animation"
)
ROOT_MATRIX_UNSUPPORTED_ERROR: Final[str] = (
    "Root matrix nodes are not supported for JSON export"
)
ROTATION_CHANNELS_ONLY_ERROR: Final[str] = (
    "Only in-place rotation animations are supported; root translations "
    "and scale channels are forbidden"
)
ROTATION_KEYS_REQUIRED_ERROR: Final[str] = (
    "At least two rotational keys are required"
)
SKINNED_ARMATURE_COUNT_ERROR: Final[str] = "Expected one skinned armature"
SOURCE_REST_POSE_ERROR: Final[str] = (
    "Rest pose mismatch: JSON was not authored for this source humanoid rig"
)
SPARSE_ACCESSOR_UNSUPPORTED_ERROR: Final[str] = (
    "Sparse glTF accessors not supported"
)
TRUNCATED_GLB_CHUNK_ERROR: Final[str] = "Truncated GLB chunk"
UNEXPECTED_ANIMATED_NODE_ERROR: Final[str] = "Unexpected animated node: {name}"
UNSUPPORTED_GLTF_INTERPOLATION_ERROR: Final[str] = (
    "Unsupported glTF interpolation: {interpolation}"
)
VALIDATE_MOTION_JSON_HELP: Final[str] = "Validate motion JSON"
ANIMATED_JOINTS_MUST_USE_GL_ERROR: Final[str] = (
    "Animated joints must use glTF TRS transforms rather than matrix nodes"
)
EVERY_SKIN_JOINT_MUST_HAVE_ERROR: Final[str] = (
    "Every skin joint must have a nonempty name"
)
