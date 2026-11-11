"""Type glTF records while preserving extension fields and numeric values."""

from enum import IntEnum, StrEnum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from src.models.base import FrozenModel
from src.utils.constants import (
    ALLOW,
    BUFFER_VIEW,
    BUFFER_VIEWS,
    BYTE_LENGTH_KEY,
    BYTE_OFFSET_KEY,
    BYTE_STRIDE,
    COMPONENT_TYPE,
    CUBICSPLINE,
    INVERSE_BIND_MATRICES,
    LINEAR,
    MAT4,
    MOTION,
    SCALAR,
    STEP,
    VEC2,
    VEC3,
    VEC4,
)


class ComponentType(IntEnum):
    """Identify glTF accessor component encodings."""

    BYTE = 5120  # noqa: TYP001, RUF100
    UNSIGNED_BYTE = 5121  # noqa: TYP001, RUF100
    SHORT = 5122  # noqa: TYP001, RUF100
    UNSIGNED_SHORT = 5123  # noqa: TYP001, RUF100
    UNSIGNED_INT = 5125  # noqa: TYP001, RUF100
    FLOAT = 5126  # noqa: TYP001, RUF100


class AccessorKind(StrEnum):
    """Identify supported glTF accessor shapes."""

    SCALAR = SCALAR  # noqa: TYP001, RUF100
    VEC2 = VEC2  # noqa: TYP001, RUF100
    VEC3 = VEC3  # noqa: TYP001, RUF100
    VEC4 = VEC4  # noqa: TYP001, RUF100
    MAT4 = MAT4  # noqa: TYP001, RUF100


class Interpolation(StrEnum):
    """Identify glTF animation interpolation modes."""

    LINEAR = LINEAR  # noqa: TYP001, RUF100
    STEP = STEP  # noqa: TYP001, RUF100
    CUBICSPLINE = CUBICSPLINE  # noqa: TYP001, RUF100


class GltfRecord(BaseModel):
    """Preserve unknown glTF extensions and original integer/float values."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra=ALLOW, populate_by_name=True
    )


class Node(GltfRecord):
    """Describe a named joint or scene node."""

    name: str | None = None
    children: list[int] = Field(default_factory=list[int])
    translation: list[int | float] = Field(
        default_factory=lambda: list[int | float]([0, 0, 0])
    )
    rotation: list[int | float] = Field(
        default_factory=lambda: list[int | float]([0, 0, 0, 1])
    )
    scale: list[int | float] = Field(
        default_factory=lambda: list[int | float]([1, 1, 1])
    )
    matrix: list[int | float] | None = None


class Buffer(GltfRecord):
    """Describe the size of an embedded binary buffer."""

    byte_length: int = Field(alias=BYTE_LENGTH_KEY)


class BufferView(GltfRecord):
    """Locate a contiguous or interleaved region in the binary buffer."""

    buffer: int
    byte_offset: int = Field(default=0, alias=BYTE_OFFSET_KEY)
    byte_length: int = Field(alias=BYTE_LENGTH_KEY)
    byte_stride: int | None = Field(default=None, alias=BYTE_STRIDE)


class Accessor(GltfRecord):
    """Describe a typed view over binary components."""

    buffer_view: int = Field(alias=BUFFER_VIEW)
    component_type: ComponentType = Field(alias=COMPONENT_TYPE)
    count: int
    type: AccessorKind
    byte_offset: int = Field(default=0, alias=BYTE_OFFSET_KEY)
    sparse: dict[str, JsonValue] | None = None
    min: list[int | float] | None = None
    max: list[int | float] | None = None


class Sampler(GltfRecord):
    """Connect animation timestamps and values."""

    input: int
    output: int
    interpolation: Interpolation = Interpolation.LINEAR


class Target(GltfRecord):
    """Identify the animated property of a glTF node."""

    node: int
    path: str


class Channel(GltfRecord):
    """Associate a target property with an animation sampler."""

    sampler: int
    target: Target


class Animation(GltfRecord):
    """Collect the sampler/channel pairs of one animation."""

    name: str = MOTION
    samplers: list[Sampler] = Field(default_factory=list[Sampler])
    channels: list[Channel] = Field(default_factory=list[Channel])


class Scene(GltfRecord):
    """List the scene's root nodes."""

    nodes: list[int]


class Skin(GltfRecord):
    """List joints participating in one skinned armature."""

    joints: list[int]
    inverse_bind_matrices: int | None = Field(
        default=None, alias=INVERSE_BIND_MATRICES
    )
    skeleton: int | None = None


class Asset(GltfRecord):
    """Keep application metadata alongside the original glTF metadata."""

    extras: dict[str, JsonValue] = Field(default_factory=dict)


class RestJoint(FrozenModel):
    """Describe the canonical joint record included in the rig signature."""

    name: str | None
    parent: str | None
    translation: list[int | float]
    rotation: list[int | float]
    scale: list[int | float]


class GltfDocument(GltfRecord):
    """Validate the records used by motion without dropping mesh payloads."""

    asset: Asset
    nodes: list[Node]
    buffers: list[Buffer]
    buffer_views: list[BufferView] = Field(alias=BUFFER_VIEWS)
    accessors: list[Accessor]
    scenes: list[Scene]
    scene: int = 0
    skins: list[Skin] = Field(default_factory=list[Skin])
    animations: list[Animation] = Field(default_factory=list[Animation])
