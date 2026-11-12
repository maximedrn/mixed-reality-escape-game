"""Publish a GLB only after reading back its embedded animation."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final

from numpy import allclose, asarray, float64
from numpy.linalg import norm
from numpy.typing import NDArray

from src.models.build import BuildRequest, BuildResult, PreparedBuild
from src.models.constraints import ConstraintResult
from src.models.motion import Motion
from src.services.constraints import constrain_motion
from src.services.glb import Glb, build_animated_glb, sampled_animation
from src.services.motion_io import load_motion, validate_trajectories
from src.utils.constants import (
    ANIMATED_GLB,
    CLIP_FIELD,
    NAME_FIELD,
    TEMPORARY_DIRECTORY_PREFIX,
)
from src.utils.messages import (
    OUTPUT_ANIMATION_CONTENT_ERROR,
    OUTPUT_ANIMATION_COUNT_ERROR,
)

ROTATION_MATCH_TOLERANCE: Final[float] = 1e-6


def validate_export(path: Path, motion: Motion) -> None:
    """Read the staged GLB and require the requested usable animation.

    :param path: Temporary binary artifact awaiting publication.
    :type path: Path
    :param motion: Requested clip and local rotation samples.
    :type motion: Motion
    :return: No return value.
    :rtype: None
    :raises RuntimeError: The embedded animation is missing or invalid.
    """
    try:
        artifact: Glb = Glb(path)
        if len(artifact.data.animations) != 1:
            raise ValueError(OUTPUT_ANIMATION_COUNT_ERROR)
        names: list[str]
        rotations: NDArray[float64]
        frames: int
        names, rotations, frames = sampled_animation(artifact, motion.clip.fps)
        if (
            names != motion.rig_pose.bone_names
            or frames != motion.frame_count
            or artifact.data.animations[0].name != motion.clip.name
        ):
            raise ValueError(OUTPUT_ANIMATION_CONTENT_ERROR)
        expected: NDArray[float64] = asarray(
            motion.rig_pose.rotations_xyzw, dtype=float64
        )
        expected /= norm(expected, axis=2, keepdims=True)
        if not allclose(
            abs((rotations * expected).sum(axis=2)),
            1,
            rtol=0,
            atol=ROTATION_MATCH_TOLERANCE,
        ):
            raise ValueError(OUTPUT_ANIMATION_CONTENT_ERROR)
    except (ValueError, IndexError, KeyError) as error:
        raise RuntimeError(OUTPUT_ANIMATION_CONTENT_ERROR) from error


def prepare_build(request: BuildRequest) -> PreparedBuild:
    """Validate and constrain the clip before creating output files.

    :param request: Existing inputs and the GLB destination.
    :type request: BuildRequest
    :return: The validated clip ready for publication.
    :rtype: PreparedBuild
    """
    motion: Motion = load_motion(request.animation)
    validate_trajectories(request.model, motion)
    changed: int = 0
    if request.constraints is not None:
        result: ConstraintResult = constrain_motion(
            request.model, motion, request.constraints
        )
        motion = result.motion
        changed = result.changed_samples
    if request.name is not None:
        payload: dict[str, object] = motion.model_dump()
        clip: dict[str, object] = motion.clip.model_dump()
        clip[NAME_FIELD] = request.name
        payload[CLIP_FIELD] = clip
        motion = Motion.model_validate(payload)
    return PreparedBuild(
        request=request, motion=motion, constrained_samples=changed
    )


def publish_build(prepared: PreparedBuild) -> BuildResult:
    """Write and atomically publish one verified animated GLB.

    :param prepared: Validated source paths, motion and limit statistics.
    :type prepared: PreparedBuild
    :return: The published GLB file and applied limit statistics.
    :rtype: BuildResult
    """
    request: BuildRequest = prepared.request
    motion: Motion = prepared.motion
    request.output_glb.parent.mkdir(parents=True, exist_ok=True)
    temporary: str
    with TemporaryDirectory(
        prefix=TEMPORARY_DIRECTORY_PREFIX, dir=request.output_glb.parent
    ) as temporary:
        staged: Path = Path(temporary) / ANIMATED_GLB
        build_animated_glb(request.model, motion, staged)
        validate_export(staged, motion)
        staged.replace(request.output_glb)
    return BuildResult(
        glb=request.output_glb,
        constrained_samples=prepared.constrained_samples,
    )


def build(request: BuildRequest) -> BuildResult:
    """Prepare and publish a single verified animated GLB.

    :param request: Existing inputs and the GLB destination.
    :type request: BuildRequest
    :return: The published GLB file and applied limit statistics.
    :rtype: BuildResult
    """
    return publish_build(prepare_build(request))
