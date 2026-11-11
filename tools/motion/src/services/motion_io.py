"""Import and export FreeMoCap-shaped JSON motion clips."""

from __future__ import annotations

from json import dumps
from pathlib import Path
from typing import Final

from numpy import absolute, allclose, asarray, float64
from numpy.linalg import norm
from numpy.typing import NDArray

from src.models.gltf import Node
from src.models.motion import (
    ClipInfo,
    CoordinateSystem,
    Marker,
    Motion,
    RigPose,
)
from src.services.glb import Glb, marker_trajectories, sampled_animation
from src.utils.constants import (
    JSON_MODE,
    NEWLINE,
    TEXT_ENCODING,
)
from src.utils.messages import (
    ANIMATED_REST_POSE_ERROR,
    ANIMATION_LOOP_ERROR,
    FPS_RANGE_ERROR,
    GLB_SCENE_ROOTS_DIFFER_ERROR,
    HORIZONTAL_ROOT_OFFSET_ERROR,
    INCONSISTENT_GROUND_OFFSET_ERROR,
    MARKER_POSE_MISMATCH_ERROR,
    MOTION_REST_POSE_ERROR,
    ROOT_MATRIX_UNSUPPORTED_ERROR,
)

DEFAULT_FPS: Final[int] = 24
ROOT_OFFSET_TOLERANCE: Final[float] = 1e-05
MAX_MARKER_ERROR_M: Final[float] = 0.001

LOOP_DOT_TOLERANCE: Final[float] = 0.0001
MILLIMETERS_PER_METER: Final[int] = 1000


def load_motion(path: Path) -> Motion:
    """Load and strictly validate one motion JSON.

    :param path: Source or destination file path.
    :type path: Path
    :return: Load and strictly validate one motion JSON.
    :rtype: Motion
    """
    return Motion.model_validate_json(path.read_text(TEXT_ENCODING))


def export_motion(
    animation_file: Path,
    base_file: Path,
    output_file: Path,
    fps: int = DEFAULT_FPS,
) -> Motion:
    """Convert the validated in-place GLB into a portable JSON clip.

    :param animation_file: Animation file.
    :type animation_file: Path
    :param base_file: Base file.
    :type base_file: Path
    :param output_file: Output file.
    :type output_file: Path
    :param fps: Sampling rate in frames per second.
    :type fps: int
    :return: Convert the validated in-place GLB into a portable JSON clip.
    :rtype: Motion
    """
    if fps <= 0:
        raise ValueError(FPS_RANGE_ERROR)
    base_glb: Glb = Glb(base_file)
    animated_glb: Glb = Glb(animation_file)
    if base_glb.signature() != animated_glb.signature():
        raise ValueError(ANIMATED_REST_POSE_ERROR)
    bones: list[str]
    rotations: NDArray[float64]
    _count: int
    bones, rotations, _count = sampled_animation(animated_glb, fps)
    markers: list[Marker] = [
        Marker(name=name, bone=name) for name in base_glb.joint_names
    ]
    positions: NDArray[float64] = marker_trajectories(
        animated_glb, [marker.bone for marker in markers], bones, rotations
    )
    ground_offset: float = _ground_offset(base_glb, animated_glb)

    start_rotations: NDArray[float64] = rotations[0]
    end_rotations: NDArray[float64] = rotations[-1]
    looping: bool = bool(
        allclose(
            absolute((start_rotations * end_rotations).sum(axis=1)),
            1.0,
            atol=LOOP_DOT_TOLERANCE,
        )
    )
    name: str = animated_glb.data.animations[0].name
    motion: Motion = Motion(
        schema_version=1,
        clip=ClipInfo(name=name, fps=fps, loop=looping, in_place=True),
        coordinates=CoordinateSystem(),
        source_rig_signature=base_glb.signature(),
        markers=markers,
        positions_xyz=positions.tolist(),
        rig_pose=RigPose(bone_names=bones, rotations_xyzw=rotations.tolist()),
        ground_offset_y=ground_offset,
    )
    if motion.clip.loop:
        starts: NDArray[float64] = asarray(
            motion.rig_pose.rotations_xyzw[0], dtype=float64
        )
        ends: NDArray[float64] = asarray(
            motion.rig_pose.rotations_xyzw[-1], dtype=float64
        )
        closed: NDArray[float64] = absolute((starts * ends).sum(axis=1))
        if not allclose(closed, 1.0, atol=LOOP_DOT_TOLERANCE):
            raise ValueError(ANIMATION_LOOP_ERROR)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        dumps(motion.model_dump(mode=JSON_MODE), indent=2, ensure_ascii=False)
        + NEWLINE,
        encoding=TEXT_ENCODING,
    )
    return motion


def validate_trajectories(base_file: Path, motion: Motion) -> float:
    """Verify that the marker data matches the authoritative quaternion pose.

    Prevents silent edits to markers with no corresponding rig transforms.
    Return the maximum joint-head position error (metres).

    :param base_file: Base file.
    :type base_file: Path
    :param motion: Validated marker and joint motion.
    :type motion: Motion
    :return: Verify that the marker data matches the authoritative quaternion
        pose.
    :rtype: float
    """
    base_glb: Glb = Glb(base_file)
    if base_glb.signature() != motion.source_rig_signature:
        raise ValueError(MOTION_REST_POSE_ERROR)
    pose: NDArray[float64] = asarray(
        motion.rig_pose.rotations_xyzw, dtype=float64
    )
    expected: NDArray[float64] = marker_trajectories(
        base_glb,
        [m.bone for m in motion.markers],
        motion.rig_pose.bone_names,
        pose,
    )
    expected[:, :, 1] += motion.ground_offset_y
    actual: NDArray[float64] = asarray(motion.positions_xyz, dtype=float64)
    error: float = float(norm(expected - actual, axis=2).max())
    if error > MAX_MARKER_ERROR_M:
        raise ValueError(
            MARKER_POSE_MISMATCH_ERROR.format(
                value=error * MILLIMETERS_PER_METER
            )
        )
    return error


def _ground_offset(base_glb: Glb, animated_glb: Glb) -> float:
    """Verify and return the shared vertical offset of the scene roots.

    :param base_glb: Static source rig.
    :type base_glb: Glb
    :param animated_glb: Animated rig to compare.
    :type animated_glb: Glb
    :return: Consistent vertical offset in metres.
    :rtype: float
    """
    root_ids: list[int] = base_glb.data.scenes[base_glb.data.scene].nodes
    animated_roots: list[int] = animated_glb.data.scenes[
        animated_glb.data.scene
    ].nodes
    if root_ids != animated_roots:
        raise ValueError(GLB_SCENE_ROOTS_DIFFER_ERROR)
    offsets: list[float] = []
    node_id: int
    for node_id in root_ids:
        base: Node = base_glb.data.nodes[node_id]
        animated: Node = animated_glb.data.nodes[node_id]
        if base.matrix is not None or animated.matrix is not None:
            raise ValueError(ROOT_MATRIX_UNSUPPORTED_ERROR)
        base_xyz: NDArray[float64] = asarray(base.translation, dtype=float64)
        anim_xyz: NDArray[float64] = asarray(
            animated.translation, dtype=float64
        )
        delta: NDArray[float64] = anim_xyz - base_xyz
        if (
            abs(delta[0]) > ROOT_OFFSET_TOLERANCE
            or abs(delta[2]) > ROOT_OFFSET_TOLERANCE
        ):
            raise ValueError(HORIZONTAL_ROOT_OFFSET_ERROR)
        offsets.append(float(delta[1]))
    if max(offsets) - min(offsets) > ROOT_OFFSET_TOLERANCE:
        raise ValueError(INCONSISTENT_GROUND_OFFSET_ERROR)

    return float(offsets[0])
