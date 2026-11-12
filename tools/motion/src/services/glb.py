"""Minimal, deterministic glTF/GLB reader and animation writer.

The module changes neither vertex data nor skin weights. It appends rotation
animation accessors to the existing binary buffer and preserves all mesh data.
"""

from __future__ import annotations

from hashlib import sha256
from json import dumps
from pathlib import Path
from struct import pack, unpack_from
from typing import BinaryIO, Final, Literal, Self

from numpy import (
    allclose,
    arange,
    asarray,
    clip,
    diag,
    dot,
    dtype,
    empty,
    eye,
    float32,
    float64,
    generic,
    int8,
    int16,
    interp,
    intp,
    isfinite,
    ndarray,
    searchsorted,
    stack,
    uint8,
    uint16,
    uint32,
)
from numpy.linalg import det, norm
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation, Slerp

from src.models.gltf import (
    Accessor,
    AccessorKind,
    Animation,
    BufferView,
    Channel,
    ComponentType,
    GltfDocument,
    Interpolation,
    Node,
    RestJoint,
    Sampler,
    Target,
)
from src.models.motion import Marker, Motion
from src.utils.constants import (
    BINARY_WRITE_MODE,
    BUFFER,
    BUFFER_VIEW,
    BYTE_LENGTH_KEY,
    BYTE_OFFSET_KEY,
    BYTE_PADDING,
    CHUNK_FORMAT,
    COLON,
    COMMA,
    COMPONENT_TYPE,
    COUNT,
    FLOAT32_LE,
    GLB_MAGIC,
    GLTF_MAXIMUM_KEY,
    GLTF_MINIMUM_KEY,
    HEADER_FORMAT,
    JOINT_NAME_SUFFIX,
    JOINT_NAME_TEMPLATE,
    JSON_MODE,
    LITTLE_ENDIAN,
    MATRIX_KEY,
    MOTION_METADATA_TEMPLATE,
    MOTION_SCHEMA_VERSION,
    RIGHT,
    ROTATION_PATH,
    SCALE_KEY,
    TEXT_ENCODING,
    TRANSLATION_KEY,
    TYPE,
    ZERO_BYTE,
    C,
    F,
)
from src.utils.messages import (
    ANIMATED_BASE_MODEL_ERROR,
    ANIMATED_BONE_NOT_FOUND_ERROR,
    ANIMATED_JOINTS_MUST_USE_GL_ERROR,
    CLIP_TIMING_ERROR,
    DUPLICATE_TRANSFORM_CHANNEL_ERROR,
    EMBEDDED_BUFFER_REQUIRED_ERROR,
    EVERY_SKIN_JOINT_MUST_HAVE_ERROR,
    FPS_RANGE_ERROR,
    GLB_CHUNKS_REQUIRED_ERROR,
    INPUT_ANIMATION_COUNT_ERROR,
    INVALID_GLB_HEADER_ERROR,
    MARKER_JOINT_NOT_FOUND_ERROR,
    MULTIPLE_NODE_PARENTS_ERROR,
    NODE_TRANSFORM_ERROR,
    NOT_A_GLB_FILE_ERROR,
    ROTATION_KEYS_REQUIRED_ERROR,
    SKINNED_ARMATURE_COUNT_ERROR,
    SOURCE_REST_POSE_ERROR,
    SPARSE_ACCESSOR_UNSUPPORTED_ERROR,
    TRANSFORM_KEYS_ERROR,
    TRUNCATED_GLB_CHUNK_ERROR,
    UNEXPECTED_ANIMATED_NODE_ERROR,
    UNSUPPORTED_GLTF_INTERPOLATION_ERROR,
    UNSUPPORTED_TRANSFORM_CHANNEL_ERROR,
)

HEADER_SIZE: Final[int] = 12
FRAME_TIME_TOLERANCE: Final[float] = 0.0001


MIN_GLB_BYTES: Final[int] = 20


MATRIX_Y_TRANSLATION_INDEX: Final[int] = 13


_JSON_CHUNK: Final[int] = 0x4E4F534A
_BIN_CHUNK: Final[int] = 0x004E4942
_COMPONENT_DTYPES: Final[dict[int, type[generic]]] = {
    5120: int8,
    5121: uint8,
    5122: int16,
    5123: uint16,
    5125: uint32,
    5126: float32,
}
_TYPE_SIZES: Final[dict[AccessorKind, int]] = {
    AccessorKind.SCALAR: 1,
    AccessorKind.VEC2: 2,
    AccessorKind.VEC3: 3,
    AccessorKind.VEC4: 4,
    AccessorKind.MAT4: 16,
}


GLB_VERSION: Final[int] = 2
MIN_ROTATION_KEYS: Final[int] = 2
TRANSFORM_EPSILON: Final[float] = 1e-12
TRANSFORM_ORTHOGONAL_TOLERANCE: Final[float] = 1e-8


class Glb:
    """Provide access to one binary glTF 2.0 file."""

    def __init__(self: Self, path: Path) -> None:
        """Parse GLB chunks and check structural invariants.

        :param path: Source or destination file path.
        :type path: Path
        """
        raw: bytes = path.read_bytes()
        if len(raw) < MIN_GLB_BYTES or raw[:4] != GLB_MAGIC:
            raise ValueError(NOT_A_GLB_FILE_ERROR.format(path=path))
        _magic: bytes
        version: int
        size: int
        _magic, version, size = unpack_from(HEADER_FORMAT, raw)
        if version != GLB_VERSION or size != len(raw):
            raise ValueError(INVALID_GLB_HEADER_ERROR)
        offset: int = HEADER_SIZE
        chunks: dict[int, bytes] = {}
        while offset < len(raw):
            chunk_size: int
            chunk_type: int
            chunk_size, chunk_type = unpack_from(CHUNK_FORMAT, raw, offset)
            start: int = offset + 8
            end: int = start + chunk_size
            if end > len(raw):
                raise ValueError(TRUNCATED_GLB_CHUNK_ERROR)
            chunks[chunk_type] = raw[start:end]
            offset = end
        if _JSON_CHUNK not in chunks or _BIN_CHUNK not in chunks:
            raise ValueError(GLB_CHUNKS_REQUIRED_ERROR)
        self.data: GltfDocument = GltfDocument.model_validate_json(
            chunks[_JSON_CHUNK]
        )
        self.data.nodes = [_normalize_node(node) for node in self.data.nodes]
        self._name_joints()
        self.binary: bytearray = bytearray(chunks[_BIN_CHUNK])
        if len(self.data.buffers) != 1:
            raise ValueError(EMBEDDED_BUFFER_REQUIRED_ERROR)

    @property
    def by_name(self: Self) -> dict[str, int]:
        """Map uniquely named glTF nodes to their indices.

        :return: Map uniquely named glTF nodes to their indices.
        :rtype: dict[str, int]
        """
        names: list[str] = self.joint_names
        return dict(zip(names, self.joint_indices, strict=True))

    def _name_joints(self: Self) -> None:
        """Give every skin joint a stable identifier.

        Unique source names are retained. Only skin joints participate, so
        duplicate names on unrelated meshes do not make a rig ambiguous.

        :return: No return value.
        :rtype: None
        """
        claimed: set[str] = set()
        index: int
        for index in self.joint_indices:
            node: Node = self.data.nodes[index]
            name: str = node.name or JOINT_NAME_TEMPLATE.format(index=index)
            if name in claimed:
                name = JOINT_NAME_TEMPLATE.format(index=index)
            while name in claimed:
                name += JOINT_NAME_SUFFIX
            node.name = name
            claimed.add(name)

    def parent_indices(self: Self) -> dict[int, int]:
        """Build a reverse glTF node-parent lookup.

        :return: Build a reverse glTF node-parent lookup.
        :rtype: dict[int, int]
        """
        result: dict[int, int] = {}
        index: int
        node: Node
        child: int
        for index, node in enumerate(self.data.nodes):
            for child in node.children:
                if child in result:
                    raise ValueError(MULTIPLE_NODE_PARENTS_ERROR)
                result[child] = index
        return result

    @property
    def joint_indices(self: Self) -> list[int]:
        """Return all skin joints, preserving first occurrence order.

        :return: Unique source joint indices across skinned meshes.
        :rtype: list[int]
        """
        if not self.data.skins:
            raise ValueError(SKINNED_ARMATURE_COUNT_ERROR)
        return list(
            dict.fromkeys(
                joint for skin in self.data.skins for joint in skin.joints
            )
        )

    @property
    def joint_names(self: Self) -> list[str]:
        """Require stable, unique names for the joints used by motion JSON.

        :return: Source joint names in skin order.
        :rtype: list[str]
        """
        names: list[str | None] = [
            self.data.nodes[index].name for index in self.joint_indices
        ]
        if any(not name for name in names):
            raise ValueError(EVERY_SKIN_JOINT_MUST_HAVE_ERROR)
        return [name for name in names if name is not None]

    def signature(self: Self, schema_version: Literal[1, 2] = 1) -> str:
        """Hash rest joints with versioned numeric serialization.

        Version 2 serializes all transform components as floating point.

        :param schema_version: Motion schema selecting the hash convention.
        :type schema_version: Literal[1, 2]
        :return: Rest skeleton hash excluding geometry and root height.
        :rtype: str
        """
        joints: list[int] = self.joint_indices
        parents: dict[int, int] = self.parent_indices()
        nodes: list[Node] = self.data.nodes
        payload: list[RestJoint] = []
        joint: int
        for joint in joints:
            node: Node = nodes[joint]
            parent: int | None = parents.get(joint)
            translation: list[int | float] = list(node.translation)
            if joint in self.data.scenes[self.data.scene].nodes:
                translation[1] = 0
            payload.append(
                RestJoint(
                    name=node.name,
                    parent=(
                        nodes[parent].name if parent is not None else None
                    ),
                    translation=(
                        [float(value) for value in translation]
                        if schema_version == MOTION_SCHEMA_VERSION
                        else translation
                    ),
                    rotation=(
                        [float(value) for value in node.rotation]
                        if schema_version == MOTION_SCHEMA_VERSION
                        else node.rotation
                    ),
                    scale=(
                        [float(value) for value in node.scale]
                        if schema_version == MOTION_SCHEMA_VERSION
                        else node.scale
                    ),
                )
            )
        blob: str = dumps(
            [joint.model_dump() for joint in payload],
            sort_keys=True,
            separators=(COMMA, COLON),
        )
        return sha256(blob.encode(TEXT_ENCODING)).hexdigest()

    def accessor(self: Self, index: int) -> NDArray[generic]:
        """Read a glTF accessor as a detached NumPy array.

        :param index: Index.
        :type index: int
        :return: Read a glTF accessor as a detached NumPy array.
        :rtype: NDArray[generic]
        """
        item: Accessor = self.data.accessors[index]
        if item.sparse:
            raise ValueError(SPARSE_ACCESSOR_UNSUPPORTED_ERROR)
        view: BufferView = self.data.buffer_views[item.buffer_view]
        component_dtype: dtype[generic] = dtype(
            _COMPONENT_DTYPES[item.component_type]
        ).newbyteorder(LITTLE_ENDIAN)
        width: int = _TYPE_SIZES[item.type]
        offset: int = view.byte_offset + item.byte_offset
        count: int = item.count
        stride: int = view.byte_stride or component_dtype.itemsize * width
        arr: NDArray[generic] = ndarray(
            shape=(count, width),
            dtype=component_dtype,
            buffer=self.binary,
            offset=offset,
            strides=(stride, component_dtype.itemsize),
        )
        return arr.copy()

    def add_accessor(
        self: Self, values: NDArray[generic], kind: AccessorKind
    ) -> int:
        """Append a FLOAT glTF accessor, keeping 4-byte alignment.

        :param values: Values.
        :type values: NDArray[generic]
        :param kind: Kind.
        :type kind: AccessorKind
        :return: Append a FLOAT glTF accessor, keeping 4-byte alignment.
        :rtype: int
        """
        array: NDArray[float32] = asarray(values, dtype=FLOAT32_LE).reshape(
            -1, _TYPE_SIZES[kind]
        )
        self.binary.extend(ZERO_BYTE * (-len(self.binary) % 4))
        offset: int = len(self.binary)
        self.binary.extend(array.tobytes(order=C))
        view_index: int = len(self.data.buffer_views)
        self.data.buffer_views.append(
            BufferView.model_validate(
                {
                    BUFFER: 0,
                    BYTE_OFFSET_KEY: offset,
                    BYTE_LENGTH_KEY: array.nbytes,
                }
            )
        )
        index: int = len(self.data.accessors)
        self.data.accessors.append(
            Accessor.model_validate(
                {
                    BUFFER_VIEW: view_index,
                    COMPONENT_TYPE: ComponentType.FLOAT,
                    COUNT: len(array),
                    TYPE: AccessorKind(kind),
                    GLTF_MINIMUM_KEY: array.min(axis=0).tolist(),
                    GLTF_MAXIMUM_KEY: array.max(axis=0).tolist(),
                }
            )
        )
        return index

    def write(self: Self, output: Path) -> None:
        """Write a binary glTF without modifying original vertices or skins.

        :param output: Destination file path.
        :type output: Path
        :return: No return value.
        :rtype: None
        """
        output.parent.mkdir(parents=True, exist_ok=True)
        self.binary.extend(ZERO_BYTE * (-len(self.binary) % 4))
        self.data.buffers[0].byte_length = len(self.binary)
        json_bytes: bytes = dumps(
            self.data.model_dump(
                mode=JSON_MODE, by_alias=True, exclude_unset=True
            ),
            ensure_ascii=False,
            separators=(COMMA, COLON),
        ).encode(TEXT_ENCODING)
        json_bytes += BYTE_PADDING * (-len(json_bytes) % 4)
        size: int = HEADER_SIZE + 8 + len(json_bytes) + 8 + len(self.binary)
        file: BinaryIO
        with output.open(BINARY_WRITE_MODE) as file:
            file.write(pack(HEADER_FORMAT, GLB_MAGIC, GLB_VERSION, size))
            file.write(pack(CHUNK_FORMAT, len(json_bytes), _JSON_CHUNK))
            file.write(json_bytes)
            file.write(pack(CHUNK_FORMAT, len(self.binary), _BIN_CHUNK))
            file.write(self.binary)


def _sample_transform(
    glb: Glb, sampler: Sampler, timestamps: NDArray[float64], path: str
) -> NDArray[float64]:
    """Resample a rotation with SLERP or a translation with linear blending.

    :param glb: Validated binary glTF document.
    :type glb: Glb
    :param sampler: Sampler.
    :type sampler: Sampler
    :param timestamps: Timestamps.
    :type timestamps: NDArray[float64]
    :param path: Rotation or translation target property.
    :type path: str
    :return: Sampled local transform vectors.
    :rtype: NDArray[float64]
    """
    keys: NDArray[float64] = (
        glb.accessor(sampler.input).reshape(-1).astype(float64)
    )
    samples: NDArray[float64] = glb.accessor(sampler.output).astype(float64)
    interpolation: Interpolation = sampler.interpolation
    if interpolation not in (Interpolation.LINEAR, Interpolation.STEP):
        raise ValueError(
            UNSUPPORTED_GLTF_INTERPOLATION_ERROR.format(
                interpolation=interpolation
            )
        )
    if (
        samples.shape != (len(keys), 4 if path == ROTATION_PATH else 3)
        or not isfinite(samples).all()
    ):
        raise ValueError(TRANSFORM_KEYS_ERROR)
    result: NDArray[float64]
    if sampler.interpolation == Interpolation.STEP:
        indices: NDArray[intp] = searchsorted(keys, timestamps, side=RIGHT) - 1
        result = samples[clip(indices, 0, len(keys) - 1)]
    elif path == ROTATION_PATH:
        # SciPy uses (x,y,z,w), identical to glTF.
        result = Slerp(keys, Rotation.from_quat(samples))(
            clip(timestamps, keys[0], keys[-1])
        ).as_quat()
    else:
        result = stack(
            [interp(timestamps, keys, samples[:, axis]) for axis in range(3)],
            axis=1,
        )
    if path == ROTATION_PATH:
        index: int
        for index in range(1, len(result)):
            if dot(result[index - 1], result[index]) < 0:
                result[index] = -result[index]
    return result


def _animation_channels(
    glb: Glb, fps: int, path: str
) -> tuple[list[tuple[str, Sampler]], NDArray[float64]]:
    """Validate all transform channels and share their complete timeline.

    :param glb: Validated binary glTF document.
    :type glb: Glb
    :param fps: Sampling rate in frames per second.
    :type fps: int
    :param path: Transform property to collect.
    :type path: str
    :return: Selected joint samplers and the complete animation timeline.
    :rtype: tuple[list[tuple[str, Sampler]], NDArray[float64]]
    """
    if fps <= 0:
        raise ValueError(FPS_RANGE_ERROR)
    animations: list[Animation] = glb.data.animations
    if len(animations) != 1:
        raise ValueError(INPUT_ANIMATION_COUNT_ERROR)
    animation: Animation = animations[0]
    channels: list[Channel] = animation.channels
    samplers: list[Sampler] = animation.samplers
    selected: list[tuple[str, Sampler]] = []
    seen: set[tuple[int, str]] = set()
    max_time: float = 0.0
    channel: Channel
    for channel in channels:
        target: Target = channel.target
        if target.path not in (ROTATION_PATH, TRANSLATION_KEY):
            raise ValueError(UNSUPPORTED_TRANSFORM_CHANNEL_ERROR)
        identity: tuple[int, str] = (target.node, target.path)
        if identity in seen:
            raise ValueError(DUPLICATE_TRANSFORM_CHANNEL_ERROR)
        seen.add(identity)
        name: str | None = glb.data.nodes[target.node].name
        if name is None or name not in glb.joint_names:
            raise ValueError(UNEXPECTED_ANIMATED_NODE_ERROR.format(name=name))
        sampler: Sampler = samplers[channel.sampler]
        times: NDArray[float64] = (
            glb.accessor(sampler.input).flatten().astype(float64)
        )
        if (
            len(times) < MIN_ROTATION_KEYS
            or not isfinite(times).all()
            or times[0] < 0
            or (times[1:] <= times[:-1]).any()
        ):
            raise ValueError(TRANSFORM_KEYS_ERROR)
        max_time = max(max_time, float(times[-1]))
        if target.path == path:
            selected.append((name, sampler))
    frames: int = round(max_time * fps) + 1
    times = arange(frames, dtype=float) / fps
    if abs(times[-1] - max_time) > FRAME_TIME_TOLERANCE:
        raise ValueError(CLIP_TIMING_ERROR)
    return selected, times


def sampled_animation(
    glb: Glb, fps: int
) -> tuple[list[str], NDArray[float64], int]:
    """Return bone-name order and XYZW rotations sampled at the given FPS.

    :param glb: Validated binary glTF document.
    :type glb: Glb
    :param fps: Sampling rate in frames per second.
    :type fps: int
    :return: Joint names, local rotations and the complete frame count.
    :rtype: tuple[list[str], NDArray[float64], int]
    """
    channels: list[tuple[str, Sampler]]
    times: NDArray[float64]
    channels, times = _animation_channels(glb, fps, ROTATION_PATH)
    if not channels:
        raise ValueError(ROTATION_KEYS_REQUIRED_ERROR)
    poses: NDArray[float64] = stack(
        [
            _sample_transform(glb, sampler, times, ROTATION_PATH)
            for _name, sampler in channels
        ],
        axis=1,
    )
    return [name for name, _sampler in channels], poses, len(times)


def sampled_translations(
    glb: Glb, fps: int, ground_offset_y: float = 0.0
) -> tuple[list[str], NDArray[float64], int]:
    """Read absolute local translations, optionally removing root grounding.

    :param glb: Validated binary glTF document.
    :type glb: Glb
    :param fps: Sampling rate in frames per second.
    :type fps: int
    :param ground_offset_y: Ground offset baked into translated scene roots.
    :type ground_offset_y: float
    :return: Joint names, local translations and the complete frame count.
    :rtype: tuple[list[str], NDArray[float64], int]
    """
    channels: list[tuple[str, Sampler]]
    times: NDArray[float64]
    channels, times = _animation_channels(glb, fps, TRANSLATION_KEY)
    names: list[str] = [name for name, _sampler in channels]
    poses: NDArray[float64] = (
        stack(
            [
                _sample_transform(glb, sampler, times, TRANSLATION_KEY)
                for _name, sampler in channels
            ],
            axis=1,
        )
        if channels
        else empty((len(times), 0, 3))
    )
    index: int
    name: str
    for index, name in enumerate(names):
        if glb.by_name[name] in glb.data.scenes[glb.data.scene].nodes:
            poses[:, index, 1] -= ground_offset_y
    return names, poses, len(times)


def marker_trajectories(
    glb: Glb,
    marker_bones: list[str],
    bone_names: list[str],
    rotation_frames: NDArray[float64],
    translation_bone_names: list[str] | None = None,
    translation_frames: NDArray[float64] | None = None,
) -> NDArray[float64]:
    """Evaluate glTF joint-head XYZ for every frame in metres.

    :param glb: Validated binary glTF document.
    :type glb: Glb
    :param marker_bones: Marker bones.
    :type marker_bones: list[str]
    :param bone_names: Bone names.
    :type bone_names: list[str]
    :param rotation_frames: Rotation frames.
    :type rotation_frames: NDArray[float64]
    :param translation_bone_names: Independently animated translation joints.
    :type translation_bone_names: list[str] | None
    :param translation_frames: Absolute local XYZ samples in metres.
    :type translation_frames: NDArray[float64] | None
    :return: Evaluate glTF joint-head XYZ for every frame in metres.
    :rtype: NDArray[float64]
    """
    indices: dict[str, int] = glb.by_name
    name: str
    for name in [*bone_names, *(translation_bone_names or [])]:
        if name not in indices:
            raise ValueError(ANIMATED_BONE_NOT_FOUND_ERROR.format(name=name))
    parents: dict[int, int] = glb.parent_indices()
    nodes: list[Node] = glb.data.nodes
    order: list[int] = []

    def visit(node_id: int) -> None:
        """Append a subtree in parent-first order.

        :param node_id: Root node of the subtree.
        :type node_id: int
        :return: No return value.
        :rtype: None
        """
        order.append(node_id)
        child: int
        for child in nodes[node_id].children:
            visit(child)

    root: int
    for root in (index for index in range(len(nodes)) if index not in parents):
        visit(root)

    base_transforms: list[NDArray[float64]] = [
        _local_transform(node) for node in nodes
    ]
    animated_node_ids: list[int] = [indices[name] for name in bone_names]
    marker_node_ids: list[int] = [indices[name] for name in marker_bones]
    positions: NDArray[float64] = empty(
        (len(rotation_frames), len(marker_node_ids), 3)
    )
    frame_id: int
    frame_rotations: NDArray[float64]
    for frame_id, frame_rotations in enumerate(rotation_frames):
        world_t: list[NDArray[float64]] = _evaluate_frame(
            nodes,
            parents,
            order,
            base_transforms,
            animated_node_ids,
            frame_rotations,
            {
                indices[name]: translation_frames[frame_id, column]
                for column, name in enumerate(translation_bone_names or [])
            }
            if translation_frames is not None
            else {},
        )
        positions[frame_id] = asarray(
            [world_t[joint] for joint in marker_node_ids]
        )
    return positions


def build_animated_glb(base: Path, motion: Motion, output: Path) -> None:
    """Apply exact local rotations and translations to the source rig.

    :param base: Static source rig file.
    :type base: Path
    :param motion: Validated marker and joint motion.
    :type motion: Motion
    :param output: Destination file path.
    :type output: Path
    :return: No return value.
    :rtype: None
    """
    glb: Glb = Glb(base)
    if glb.data.animations:
        raise ValueError(ANIMATED_BASE_MODEL_ERROR)
    if glb.signature(motion.schema_version) != motion.source_rig_signature:
        raise ValueError(SOURCE_REST_POSE_ERROR)
    indices: dict[str, int] = glb.by_name
    name: str
    marker: Marker
    root: int
    for name in [
        *motion.rig_pose.bone_names,
        *motion.rig_pose.translation_bone_names,
    ]:
        if name not in indices:
            raise ValueError(ANIMATED_BONE_NOT_FOUND_ERROR.format(name=name))
    for marker in motion.markers:
        if marker.bone not in indices:
            raise ValueError(
                MARKER_JOINT_NOT_FOUND_ERROR.format(bone=marker.bone)
            )
    original_roots: list[int] = glb.data.scenes[glb.data.scene].nodes
    for root in original_roots:
        node: Node = glb.data.nodes[root]
        if node.matrix is not None:
            node.matrix[MATRIX_Y_TRANSLATION_INDEX] += motion.ground_offset_y
        else:
            translation: list[int | float] = list(node.translation)
            translation[1] += motion.ground_offset_y
            node.translation = translation
    times: NDArray[float32] = asarray(
        arange(motion.frame_count, dtype=FLOAT32_LE) / motion.clip.fps,
        dtype=FLOAT32_LE,
    )
    input_accessor: int = glb.add_accessor(times, AccessorKind.SCALAR)
    animation: Animation = Animation(
        name=motion.clip.name, samplers=[], channels=[]
    )
    _append_transform_channels(
        glb, motion, animation, input_accessor, ROTATION_PATH
    )
    _append_transform_channels(
        glb, motion, animation, input_accessor, TRANSLATION_KEY
    )
    glb.data.animations = [animation]
    glb.data.asset.extras = dict(
        glb.data.asset.extras,
        motion=(MOTION_METADATA_TEMPLATE.format(name=motion.clip.name)),
    )
    glb.write(output)


def _append_transform_channels(
    glb: Glb,
    motion: Motion,
    animation: Animation,
    input_accessor: int,
    path: str,
) -> None:
    """Append verified local pose vectors using a shared timestamp accessor.

    :param glb: Destination rig and embedded binary buffer.
    :type glb: Glb
    :param motion: Source pose samples and ground offset.
    :type motion: Motion
    :param animation: Animation receiving the new channels.
    :type animation: Animation
    :param input_accessor: Shared timestamp accessor index.
    :type input_accessor: int
    :param path: Rotation or translation target property.
    :type path: str
    :return: No return value.
    :rtype: None
    """
    rotation: bool = path == ROTATION_PATH
    names: list[str] = (
        motion.rig_pose.bone_names
        if rotation
        else motion.rig_pose.translation_bone_names
    )
    values: NDArray[float32] = asarray(
        motion.rig_pose.rotations_xyzw
        if rotation
        else motion.rig_pose.translations_xyz,
        dtype=FLOAT32_LE,
    )
    bone_id: int
    bone_name: str
    for bone_id, bone_name in enumerate(names):
        keys: NDArray[float32] = values[:, bone_id].copy()
        if rotation:
            frame: int
            for frame in range(1, len(keys)):
                if dot(keys[frame - 1], keys[frame]) < 0:
                    keys[frame] = -keys[frame]
            keys /= norm(keys, axis=1, keepdims=True)
        elif glb.by_name[bone_name] in glb.data.scenes[glb.data.scene].nodes:
            keys[:, 1] += motion.ground_offset_y
        accessor: int = glb.add_accessor(
            keys, AccessorKind.VEC4 if rotation else AccessorKind.VEC3
        )
        channel_id: int = len(animation.samplers)
        animation.samplers.append(
            Sampler(
                input=input_accessor,
                output=accessor,
                interpolation=Interpolation.LINEAR,
            )
        )
        animation.channels.append(
            Channel(
                sampler=channel_id,
                target=Target(node=glb.by_name[bone_name], path=path),
            )
        )


def _local_transform(
    node: Node, rotation: Rotation | None = None
) -> NDArray[float64]:
    """Build a local affine transform, preserving static scale and matrices.

    :param node: Source glTF node.
    :type node: Node
    :param rotation: Optional sampled local rotation replacing the rest value.
    :type rotation: Rotation | None
    :return: Column-vector affine transform.
    :rtype: NDArray[float64]
    :raises ValueError: A matrix node is animated without TRS decomposition.
    """
    if node.matrix is not None:
        if rotation is not None:
            raise ValueError(ANIMATED_JOINTS_MUST_USE_GL_ERROR)
        return asarray(node.matrix, dtype=float64).reshape(4, 4, order=F)
    transform: NDArray[float64] = eye(4, dtype=float64)
    orientation: Rotation = (
        rotation if rotation is not None else Rotation.from_quat(node.rotation)
    )
    transform[:3, :3] = orientation.as_matrix() @ diag(
        asarray(node.scale, dtype=float64)
    )
    transform[:3, 3] = node.translation
    return transform


def _evaluate_frame(
    nodes: list[Node],
    parents: dict[int, int],
    order: list[int],
    base_transforms: list[NDArray[float64]],
    animated_node_ids: list[int],
    frame_rotations: NDArray[float64],
    translations: dict[int, NDArray[float64]],
) -> list[NDArray[float64]]:
    """Evaluate affine joint transforms for one sampled frame.

    :param nodes: Source glTF nodes.
    :type nodes: list[Node]
    :param parents: Reverse hierarchy lookup.
    :type parents: dict[int, int]
    :param order: Parent-first traversal order.
    :type order: list[int]
    :param base_transforms: Static local affine transforms.
    :type base_transforms: list[NDArray[float64]]
    :param animated_node_ids: Joint indices receiving rotation samples.
    :type animated_node_ids: list[int]
    :param frame_rotations: Local XYZW quaternions for this frame.
    :type frame_rotations: NDArray[float64]
    :param translations: Absolute local XYZ keyed by translated node index.
    :type translations: dict[int, NDArray[float64]]
    :return: Joint-head positions in world space.
    :rtype: list[NDArray[float64]]
    """
    local: list[NDArray[float64]] = [
        matrix.copy() for matrix in base_transforms
    ]
    node_id: int
    quat: NDArray[float64]
    for node_id, quat in zip(animated_node_ids, frame_rotations, strict=True):
        local[node_id] = _local_transform(
            nodes[node_id], Rotation.from_quat(quat)
        )
    translation: NDArray[float64]
    for node_id, translation in translations.items():
        local[node_id][:3, 3] = translation
    world: list[NDArray[float64]] = [eye(4, dtype=float64) for _ in nodes]
    for node_id in order:
        parent: int | None = parents.get(node_id)
        world[node_id] = (
            local[node_id]
            if parent is None
            else world[parent] @ local[node_id]
        )
    return [matrix[:3, 3] for matrix in world]


def _normalize_node(node: Node) -> Node:
    """Decompose a static matrix into the TRS form required by joint animation.

    :param node: Original glTF node, including opaque extension fields.
    :type node: Node
    :return: Equivalent validated node with an animatable TRS representation.
    :rtype: Node
    :raises ValueError: The matrix contains shear or a singular scale.
    """
    if node.matrix is None:
        return node
    transform: NDArray[float64] = asarray(node.matrix, dtype=float64).reshape(
        4, 4, order=F
    )
    scale: NDArray[float64] = norm(transform[:3, :3], axis=0)
    if any(abs(value) < TRANSFORM_EPSILON for value in scale):
        raise ValueError(NODE_TRANSFORM_ERROR)
    if det(transform[:3, :3]) < 0:
        scale[0] *= -1
    basis: NDArray[float64] = transform[:3, :3] / scale
    if not allclose(
        basis.T @ basis, eye(3), atol=TRANSFORM_ORTHOGONAL_TOLERANCE
    ):
        raise ValueError(NODE_TRANSFORM_ERROR)
    payload: dict[str, object] = node.model_dump(
        mode=JSON_MODE, exclude_unset=True
    )
    payload.pop(MATRIX_KEY)
    payload[TRANSLATION_KEY] = transform[:3, 3].tolist()
    payload[ROTATION_PATH] = Rotation.from_matrix(basis).as_quat().tolist()
    payload[SCALE_KEY] = scale.tolist()
    return Node.model_validate(payload)
