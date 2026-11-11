"""Validate a FreeMoCap-shaped marker trajectory with rig pose extensions."""

from __future__ import annotations

from enum import StrEnum
from math import sqrt
from typing import Final, Literal, Self

from pydantic import Field, model_validator

from src.models.base import FrozenModel
from src.utils.constants import (
    GLTF,
    HEX_DIGITS,
    METERS_UNIT,
    POSITIVE_Z_FORWARD_AXIS,
    Y_UP_AXIS,
)
from src.utils.messages import (
    DUPLICATE_MARKER_NAMES_ERROR,
    DUPLICATE_RIG_JOINT_NAMES_ERROR,
    DUPLICATE_TRACKED_JOINTS_ERROR,
    FRAME_EXPECTED_MARKERS_ERROR,
    FRAME_EXPECTED_ROTATIONS_ERROR,
    FRAME_NON_UNIT_QUATERNION_ERROR,
    INVALID_RIG_SIGNATURE_ERROR,
    LOOP_ROTATIONS_ERROR,
    MOTION_FRAME_COUNT_ERROR,
)

MAX_FPS: Final[int] = 240
SHA256_HEX_LENGTH: Final[int] = 64
MIN_LOOP_DOT: Final[float] = 0.9999
MIN_QUATERNION_NORM: Final[float] = 0.98
MAX_QUATERNION_NORM: Final[float] = 1.02


class ClipInfo(FrozenModel):
    """Timeline and clip behavior."""

    name: str = Field(min_length=1)
    fps: int = Field(gt=0, le=MAX_FPS)
    loop: bool = True
    in_place: Literal[True] = True


class CoordinateValue(StrEnum):
    """Name the supported coordinate convention components."""

    SPACE = GLTF  # noqa: TYP001, RUF100
    UNITS = METERS_UNIT  # noqa: TYP001, RUF100
    UP = Y_UP_AXIS  # noqa: TYP001, RUF100
    FORWARD = POSITIVE_Z_FORWARD_AXIS  # noqa: TYP001, RUF100


class CoordinateSystem(FrozenModel):
    """Require the coordinate convention understood by the GLB builder."""

    space: Literal[CoordinateValue.SPACE] = CoordinateValue.SPACE
    units: Literal[CoordinateValue.UNITS] = CoordinateValue.UNITS
    up: Literal[CoordinateValue.UP] = CoordinateValue.UP
    forward: Literal[CoordinateValue.FORWARD] = CoordinateValue.FORWARD


class Marker(FrozenModel):
    """Associate a semantic tracked marker with one skin joint."""

    name: str = Field(min_length=1)
    bone: str = Field(min_length=1)


class RigPose(FrozenModel):
    """Lossless local rotations for the source humanoid skeleton."""

    bone_names: list[str] = Field(min_length=1)
    rotations_xyzw: list[list[tuple[float, float, float, float]]] = Field(
        min_length=2
    )


class Motion(FrozenModel):
    """Frame-major marker XYZ plus reversible humanoid joint rotations.

    ``positions_xyz`` has the same frame/marker/axis shape as FreeMoCap 3D
    arrays. ``rig_pose`` is a declared extension, not a native FreeMoCap
    field.
    """

    schema_version: Literal[1] = 1
    clip: ClipInfo
    coordinates: CoordinateSystem
    source_rig_signature: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    markers: list[Marker] = Field(min_length=1)
    positions_xyz: list[list[tuple[float, float, float]]] = Field(min_length=2)
    rig_pose: RigPose
    ground_offset_y: float = 0.0

    @model_validator(mode="after")
    def validate_frames(self) -> Self:
        """Refuse malformed frames, quaternions, and duplicates.

        :return: Refuse malformed frames, quaternions, and duplicates.
        :rtype: Self
        """
        frame_count: int = len(self.positions_xyz)
        marker_count: int = len(self.markers)
        if len({marker.name for marker in self.markers}) != marker_count:
            raise ValueError(DUPLICATE_MARKER_NAMES_ERROR)
        if len({marker.bone for marker in self.markers}) != marker_count:
            raise ValueError(DUPLICATE_TRACKED_JOINTS_ERROR)
        bones: list[str] = self.rig_pose.bone_names
        if len(set(bones)) != len(bones):
            raise ValueError(DUPLICATE_RIG_JOINT_NAMES_ERROR)
        if len(self.rig_pose.rotations_xyzw) != frame_count:
            raise ValueError(MOTION_FRAME_COUNT_ERROR)
        frame_number: int
        markers: list[tuple[float, float, float]]
        quats: list[tuple[float, float, float, float]]
        for frame_number, (markers, quats) in enumerate(
            zip(self.positions_xyz, self.rig_pose.rotations_xyzw, strict=True)
        ):
            if len(markers) != marker_count:
                raise ValueError(
                    FRAME_EXPECTED_MARKERS_ERROR.format(
                        frame_number=frame_number, marker_count=marker_count
                    )
                )
            if len(quats) != len(bones):
                raise ValueError(
                    FRAME_EXPECTED_ROTATIONS_ERROR.format(
                        frame_number=frame_number, bone_count=len(bones)
                    )
                )
            _validate_quaternions(quats, frame_number)
        if self.clip.loop:
            start: list[tuple[float, float, float, float]] = (
                self.rig_pose.rotations_xyzw[0]
            )
            end: list[tuple[float, float, float, float]] = (
                self.rig_pose.rotations_xyzw[-1]
            )
            _validate_loop(start, end)
        if len(self.source_rig_signature) != SHA256_HEX_LENGTH or any(
            ch not in HEX_DIGITS for ch in self.source_rig_signature
        ):
            raise ValueError(INVALID_RIG_SIGNATURE_ERROR)
        return self

    @property
    def frame_count(self) -> int:
        """Number of frame samples, including the closing loop frame.

        :return: Number of frame samples, including the closing loop frame.
        :rtype: int
        """
        return len(self.positions_xyz)


def _validate_quaternions(
    quats: list[tuple[float, float, float, float]],
    frame_number: int,
) -> None:
    """Check a frame's quaternion magnitudes.

    :param quats: Frame quaternions in XYZW order.
    :type quats: list[tuple[float, float, float, float]]
    :param frame_number: Frame identifier used in error messages.
    :type frame_number: int
    :return: No return value.
    :rtype: None
    """
    quat: tuple[float, float, float, float]
    for quat in quats:
        norm: float = sqrt(sum(component * component for component in quat))
        if not MIN_QUATERNION_NORM <= norm <= MAX_QUATERNION_NORM:
            raise ValueError(
                FRAME_NON_UNIT_QUATERNION_ERROR.format(
                    frame_number=frame_number
                )
            )


def _validate_loop(
    start: list[tuple[float, float, float, float]],
    end: list[tuple[float, float, float, float]],
) -> None:
    """Check physical rotation continuity at the loop boundary.

    :param start: First frame's quaternions.
    :type start: list[tuple[float, float, float, float]]
    :param end: Last frame's quaternions.
    :type end: list[tuple[float, float, float, float]]
    :return: No return value.
    :rtype: None
    """
    first: tuple[float, float, float, float]
    last: tuple[float, float, float, float]
    for first, last in zip(start, end, strict=True):
        dot: float = abs(
            sum(left * right for left, right in zip(first, last, strict=True))
        )
        if dot < MIN_LOOP_DOT:
            raise ValueError(LOOP_ROTATIONS_ERROR)
