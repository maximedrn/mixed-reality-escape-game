"""Bake joint limits into source-rig rotations and derived marker positions."""

from pathlib import Path
from typing import Final
from warnings import catch_warnings, filterwarnings

from numpy import asarray, clip, dot, empty, float64, isclose, repeat, zeros
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation

from src.models.constraints import (
    ConstraintResult,
    ConstraintsConfig,
    HingeJointLimit,
    JointLimit,
    LocalJointLimit,
    Vector3,
)
from src.models.motion import Motion, RigPose
from src.services.glb import Glb, marker_trajectories
from src.utils.constants import (
    EULER_AXES,
    GIMBAL_LOCK_WARNING,
    IGNORE_WARNING,
    TEXT_ENCODING,
)
from src.utils.messages import (
    HINGE_CHILD_ERROR,
    HINGE_DIRECTION_ERROR,
    UNKNOWN_LIMIT_JOINT_ERROR,
)

ANGLE_TOLERANCE_DEG: Final[float] = 1e-7
HINGE_PROBE_DEG: Final[float] = 0.1
MIN_HINGE_RESPONSE: Final[float] = 1e-10


def constrain_motion(
    base: Path, motion: Motion, path: Path
) -> ConstraintResult:
    """Clamp bind-relative rotation keys and recompute their marker samples.

    :param base: Static source rig.
    :type base: Path
    :param motion: Validated original motion.
    :type motion: Motion
    :param path: Joint-limit JSON configuration.
    :type path: Path
    :return: Constrained clip and the count of adjusted rotation samples.
    :rtype: ConstraintResult
    """
    config: ConstraintsConfig = ConstraintsConfig.model_validate_json(
        path.read_text(encoding=TEXT_ENCODING)
    )
    rig: Glb = Glb(base)
    names: list[str] = list(motion.rig_pose.bone_names)
    rotations: NDArray[float64] = asarray(
        motion.rig_pose.rotations_xyzw, dtype=float64
    )
    extra_names: list[str] = []
    name: str
    for name in config.limits:
        if name not in rig.by_name:
            raise ValueError(UNKNOWN_LIMIT_JOINT_ERROR.format(name=name))
        if name not in names:
            extra_names.append(name)
    if extra_names:
        extended: NDArray[float64] = empty(
            (motion.frame_count, len(names) + len(extra_names), 4)
        )
        extended[:, : len(names)] = rotations
        index: int
        for index, name in enumerate(extra_names, start=len(names)):
            extended[:, index] = rig.data.nodes[rig.by_name[name]].rotation
        rotations = extended
        names.extend(extra_names)
    changed: int = 0
    policy: JointLimit
    for name, policy in config.limits.items():
        index = names.index(name)
        rest: Rotation = Rotation.from_quat(
            rig.data.nodes[rig.by_name[name]].rotation
        )
        relative: Rotation = rest.inv() * Rotation.from_quat(
            rotations[:, index]
        )
        angles: NDArray[float64] = euler_angles(relative)
        lower: NDArray[float64]
        upper: NDArray[float64]
        lower, upper = rotation_bounds(rig, name, policy)
        limited: NDArray[float64] = clip(angles, lower, upper)
        changed += int(
            (~isclose(angles, limited, atol=ANGLE_TOLERANCE_DEG, rtol=0))
            .any(axis=1)
            .sum()
        )
        rotations[:, index] = (
            rest * Rotation.from_euler(EULER_AXES, limited, degrees=True)
        ).as_quat()
    positions: NDArray[float64] = marker_trajectories(
        rig,
        [marker.bone for marker in motion.markers],
        names,
        rotations,
        motion.rig_pose.translation_bone_names,
        asarray(motion.rig_pose.translations_xyz, dtype=float64),
    )
    positions[:, :, 1] += motion.ground_offset_y
    return ConstraintResult(
        motion=Motion(
            schema_version=motion.schema_version,
            clip=motion.clip,
            coordinates=motion.coordinates,
            source_rig_signature=motion.source_rig_signature,
            markers=motion.markers,
            positions_xyz=positions.tolist(),
            rig_pose=RigPose(
                bone_names=names,
                rotations_xyzw=rotations.tolist(),
                translation_bone_names=motion.rig_pose.translation_bone_names,
                translations_xyz=motion.rig_pose.translations_xyz,
            ),
            ground_offset_y=motion.ground_offset_y,
        ),
        changed_samples=changed,
    )


def euler_angles(rotation: Rotation) -> NDArray[float64]:
    """Express bind-relative rotations as extrinsic XYZ degree angles.

    :param rotation: Local rotations relative to the bind pose.
    :type rotation: Rotation
    :return: Three Euler components for each rotation sample.
    :rtype: NDArray[float64]
    """
    with catch_warnings():
        filterwarnings(IGNORE_WARNING, message=GIMBAL_LOCK_WARNING)
        return rotation.as_euler(EULER_AXES, degrees=True)


def rotation_bounds(
    rig: Glb, name: str, policy: JointLimit
) -> tuple[NDArray[float64], NDArray[float64]]:
    """Resolve static ranges or calibrate a hinge against its child joint.

    :param rig: Static source rig.
    :type rig: Glb
    :param name: Limited source joint identifier.
    :type name: str
    :param policy: Local-axis or hinge rotation limits.
    :type policy: JointLimit
    :return: Lower and upper XYZ angle bounds in degrees.
    :rtype: tuple[NDArray[float64], NDArray[float64]]
    """
    if isinstance(policy, LocalJointLimit):
        return asarray(policy.min_deg), asarray(policy.max_deg)
    lower: NDArray[float64] = repeat(-policy.lateral_slack_deg, 3)
    upper: NDArray[float64] = repeat(policy.lateral_slack_deg, 3)
    lower[policy.twist_axis] = -policy.twist_deg
    upper[policy.twist_axis] = policy.twist_deg
    direction: float = hinge_direction(rig, name, policy)
    lower[policy.hinge_axis] = (
        -policy.hyperextension_deg if direction > 0 else -policy.flexion_deg
    )
    upper[policy.hinge_axis] = (
        policy.flexion_deg if direction > 0 else policy.hyperextension_deg
    )
    return lower, upper


def hinge_direction(rig: Glb, name: str, policy: HingeJointLimit) -> float:
    """Probe flexion in the rest rig, including ancestor rotations and scale.

    :param rig: Static source rig.
    :type rig: Glb
    :param name: Hinge joint identifier.
    :type name: str
    :param policy: Axis and requested world-space bend direction.
    :type policy: HingeJointLimit
    :return: Positive or negative sign for flexion about the hinge axis.
    :rtype: float
    """
    child: str = child_joint(rig, name)
    node_id: int = rig.by_name[name]
    rest: Rotation = Rotation.from_quat(rig.data.nodes[node_id].rotation)
    probe: NDArray[float64] = zeros(3)
    probe[policy.hinge_axis] = HINGE_PROBE_DEG
    bent: Rotation = rest * Rotation.from_euler(
        EULER_AXES, probe, degrees=True
    )
    samples: NDArray[float64] = asarray(
        [[rest.as_quat()], [bent.as_quat()]], dtype=float64
    )
    positions: NDArray[float64] = marker_trajectories(
        rig, [child], [name], samples
    )
    direction: Vector3 = policy.bend_direction
    response: float = float(dot(positions[1, 0] - positions[0, 0], direction))
    if abs(response) <= MIN_HINGE_RESPONSE:
        raise ValueError(HINGE_DIRECTION_ERROR.format(name=name))
    return 1.0 if response > 0 else -1.0


def child_joint(rig: Glb, name: str) -> str:
    """Find a descendant skin joint for finite-difference hinge calibration.

    :param rig: Static source rig.
    :type rig: Glb
    :param name: Parent joint identifier.
    :type name: str
    :return: The first descendant participating in the source skin.
    :rtype: str
    """
    pending: list[int] = list(rig.data.nodes[rig.by_name[name]].children)
    indices: set[int] = set(rig.joint_indices)
    while pending:
        index: int = pending.pop(0)
        if index in indices:
            return rig.joint_names[rig.joint_indices.index(index)]
        pending.extend(rig.data.nodes[index].children)
    raise ValueError(HINGE_CHILD_ERROR.format(name=name))
