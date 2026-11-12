"""Validate bind-relative joint rotation limits and authoring metadata."""

from enum import StrEnum
from typing import Annotated, Final, Literal, Self

from pydantic import Field, JsonValue, model_validator

from src.models.base import FrozenModel
from src.models.motion import Motion
from src.utils.constants import (
    ALL_LOCAL_MODE,
    AUTO_HINGE_MODE,
    AXIS_MODE_FIELD,
)
from src.utils.messages import HINGE_AXIS_ERROR, LIMIT_ORDER_ERROR

MAX_ANGLE_DEG: Final[float] = 180.0
DIRECTION_EPSILON: Final[float] = 1e-12

type Angle = Annotated[float, Field(ge=-MAX_ANGLE_DEG, le=MAX_ANGLE_DEG)]
type PositiveAngle = Annotated[float, Field(ge=0, le=MAX_ANGLE_DEG)]
type Vector3 = tuple[float, float, float]


class LimitMode(StrEnum):
    """Identify local Euler ranges and calibrated hinge joints."""

    LOCAL = ALL_LOCAL_MODE  # noqa: TYP001, RUF100
    HINGE = AUTO_HINGE_MODE  # noqa: TYP001, RUF100


class LocalJointLimit(FrozenModel):
    """Bound extrinsic XYZ Euler angles relative to the bind pose."""

    axis_mode: Literal[LimitMode.LOCAL] = LimitMode.LOCAL
    min_deg: tuple[Angle, Angle, Angle]
    max_deg: tuple[Angle, Angle, Angle]
    group: str | None = None

    # Pydantic's MyPy plugin requires the validator mode to remain lexical.
    @model_validator(mode="after")  # noqa: WPS226
    def validate_ranges(self) -> Self:
        """Require increasing limits on every rotation axis.

        :return: The validated local rotation policy.
        :rtype: Self
        """
        if any(
            lower > upper
            for lower, upper in zip(self.min_deg, self.max_deg, strict=True)
        ):
            raise ValueError(LIMIT_ORDER_ERROR)
        return self


class HingeJointLimit(FrozenModel):
    """Calibrate flexion direction and bound twist and lateral motion."""

    axis_mode: Literal[LimitMode.HINGE] = LimitMode.HINGE
    flexion_deg: PositiveAngle
    hyperextension_deg: PositiveAngle
    lateral_slack_deg: PositiveAngle
    hinge_axis: int = Field(ge=0, le=2)
    bend_direction: Vector3
    twist_axis: int = Field(default=1, ge=0, le=2)
    twist_deg: PositiveAngle = 0
    group: str | None = None

    @model_validator(mode="after")
    def validate_axes(self) -> Self:
        """Require distinct axes and a usable flexion direction.

        :return: The validated hinge policy.
        :rtype: Self
        """
        if (
            self.hinge_axis == self.twist_axis
            or sum(value * value for value in self.bend_direction)
            <= DIRECTION_EPSILON
        ):
            raise ValueError(HINGE_AXIS_ERROR)
        return self


type JointLimit = Annotated[
    LocalJointLimit | HingeJointLimit, Field(discriminator=AXIS_MODE_FIELD)
]


class ConstraintsConfig(FrozenModel):
    """Read joint limits alongside optional rig-authoring information."""

    schema_version: Literal[1] = 1
    model: str | None = None
    character: dict[str, JsonValue] = Field(default_factory=dict)
    calibration: dict[str, JsonValue] = Field(default_factory=dict)
    ik: dict[str, JsonValue] = Field(default_factory=dict)
    limits: dict[str, JointLimit] = Field(default_factory=dict)


class ConstraintResult(FrozenModel):
    """Return constrained motion and the number of changed joint samples."""

    motion: Motion
    changed_samples: int = Field(ge=0)
