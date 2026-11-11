"""Publish a GLB only after reading back its embedded animation."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Final

from numpy import allclose, asarray, float64
from numpy.linalg import norm
from numpy.typing import NDArray

from src.models.build import BuildRequest, BuildResult
from src.models.motion import Motion
from src.services.glb import Glb, build_animated_glb, sampled_animation
from src.services.motion_io import load_motion, validate_trajectories
from src.utils.constants import ANIMATED_GLB, TEMPORARY_DIRECTORY_PREFIX
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


def build(request: BuildRequest) -> BuildResult:
    """Export and atomically publish the verified animated GLB.

    :param request: Existing inputs and the GLB destination.
    :type request: BuildRequest
    :return: The published GLB file.
    :rtype: BuildResult
    :raises RuntimeError: Export produces a missing or invalid animation.
    """
    motion: Motion = load_motion(request.animation)
    validate_trajectories(request.model, motion)
    request.output_glb.parent.mkdir(parents=True, exist_ok=True)
    temporary: str
    with TemporaryDirectory(
        prefix=TEMPORARY_DIRECTORY_PREFIX, dir=request.output_glb.parent
    ) as temporary:
        staged: Path = Path(temporary) / ANIMATED_GLB
        build_animated_glb(request.model, motion, staged)
        validate_export(staged, motion)
        staged.replace(request.output_glb)
    return BuildResult(glb=request.output_glb)
