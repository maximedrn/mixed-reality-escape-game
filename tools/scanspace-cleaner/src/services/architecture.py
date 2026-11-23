"""Retain architectural meshes and cover ScanSpace window openings."""

from collections.abc import Mapping
from pathlib import Path
from tomllib import load
from typing import cast

from numpy import asarray, column_stack, float64
from numpy.typing import NDArray
from trimesh import (
    Scene,
    Trimesh,
    load_scene,  # pyright: ignore[reportUnknownVariableType]
)
from trimesh.creation import box  # pyright: ignore[reportUnknownVariableType]
from trimesh.visual import TextureVisuals

from src.models.configuration import CleanConfig
from src.models.result import CleanResult
from src.models.scanspace import ScanStructure, WindowDefinition
from src.services.scanspace_io import load_structure
from src.utils.constants import (
    ARCHITECTURE_MESHES,
    FIRST_WINDOW_INDEX,
    GLB_SUFFIX,
    READ_BINARY_MODE,
    TRANSFORM_SIDE,
    WALL_GEOMETRY_NAME,
    WINDOW_NAME_TEMPLATE,
)
from src.utils.messages import (
    INVALID_MESH_ERROR,
    MATERIAL_REQUIRED_ERROR,
    OUTPUT_OVERLAPS_INPUT_ERROR,
    OUTPUT_SUFFIX_ERROR,
)


def clean_architecture(config_file: Path) -> CleanResult:
    """Publish a floorplan stripped of furniture and filled at its windows.

    :param config_file: TOML file defining the floorplan and patch dimensions.
    :type config_file: Path
    :return: Output path, mesh counts, and resulting scene bounds.
    :rtype: CleanResult
    """
    config_file = config_file.expanduser().resolve()
    with config_file.open(READ_BINARY_MODE) as stream:
        options: CleanConfig = CleanConfig.model_validate(load(stream))
    root: Path = config_file.parent
    source_file: Path = (root / options.input.expanduser()).resolve()
    scan_file: Path = (root / options.scan.expanduser()).resolve()
    output_file: Path = (root / options.output.expanduser()).resolve()
    if output_file.suffix.lower() != GLB_SUFFIX:
        raise ValueError(OUTPUT_SUFFIX_ERROR)
    if output_file in (config_file, source_file, scan_file):
        raise ValueError(OUTPUT_OVERLAPS_INPUT_ERROR)

    structure: ScanStructure = load_structure(scan_file)
    original: Scene = load_scene(source_file)
    cleaned: Scene = _retain_architecture(original)
    for index, window in enumerate(
        structure.windows, start=FIRST_WINDOW_INDEX
    ):
        patch: Trimesh = _window_patch(
            original, window, options.window_overlap_m, options.window_depth_m
        )
        name: str = WINDOW_NAME_TEMPLATE.format(index=index)
        cleaned.add_geometry(  # pyright: ignore[reportUnknownMemberType]
            patch, geom_name=name, node_name=name
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned.export(output_file)  # pyright: ignore[reportUnknownMemberType]
    bounds: NDArray[float64] = asarray(cleaned.bounds, dtype=float64)
    return CleanResult(
        output=output_file,
        original_faces=_face_count(original),
        clean_faces=_face_count(cleaned),
        windows_filled=len(structure.windows),
        bounds=bounds.tolist(),
        geometry={
            name: len(mesh.faces)
            for name, mesh in _scene_geometry(cleaned).items()
            if isinstance(mesh, Trimesh)
        },
    )


def _retain_architecture(original: Scene) -> Scene:
    """Copy ScanSpace wall, floor and door meshes without other furnishings.

    :param original: Source GLB scene with ScanSpace mesh identifiers.
    :type original: Scene
    :return: Scene containing only the architectural mesh copies.
    :rtype: Scene
    """
    cleaned: Scene = Scene()
    for name, original_name in ARCHITECTURE_MESHES:
        geometry: Trimesh = _mesh(original, original_name)
        cleaned.add_geometry(  # pyright: ignore[reportUnknownMemberType]
            geometry.copy(), geom_name=name, node_name=name
        )
    return cleaned


def _window_patch(
    original: Scene, window: WindowDefinition, overlap: float, depth: float
) -> Trimesh:
    """Produce a textured wall slab at one RoomPlan window transform.

    :param original: Original scene containing the wall texture.
    :type original: Scene
    :param window: Width, height and column-major world transform.
    :type window: WindowDefinition
    :param overlap: Total width and height added to the opening in metres.
    :type overlap: float
    :param depth: Wall slab thickness in metres.
    :type depth: float
    :return: Window-filling mesh using the source wall material.
    :rtype: Trimesh
    """
    wall: Trimesh = _mesh(original, WALL_GEOMETRY_NAME)
    if not isinstance(wall.visual, TextureVisuals):
        raise ValueError(MATERIAL_REQUIRED_ERROR)
    transform: NDArray[float64] = (
        asarray(window.transform, dtype=float64)
        .reshape((TRANSFORM_SIDE, TRANSFORM_SIDE))
        .T
    )
    width, height, _ = window.dimensions
    patch: Trimesh = box(
        extents=[
            width + overlap,
            height + overlap,
            depth,
        ]
    )
    vertices: NDArray[float64] = asarray(patch.vertices, dtype=float64)
    uv: NDArray[float64] = column_stack((vertices[:, 0], vertices[:, 1]))
    patch.visual = TextureVisuals(
        uv=uv,
        material=wall.visual.material,  # pyright: ignore[reportUnknownMemberType]
    )
    patch.apply_transform(transform)  # pyright: ignore[reportUnknownMemberType]
    return patch


def _mesh(scene: Scene, name: str) -> Trimesh:
    """Retrieve a named triangular mesh from a ScanSpace GLB.

    :param scene: Source ScanSpace scene.
    :type scene: Scene
    :param name: Source mesh identifier.
    :type name: str
    :return: Corresponding mesh geometry.
    :rtype: Trimesh
    """
    value: object = _scene_geometry(scene).get(name)
    if not isinstance(value, Trimesh):
        raise ValueError(INVALID_MESH_ERROR.format(name=name))
    return value


def _face_count(scene: Scene) -> int:
    """Count triangles in a scene's triangular mesh geometries.

    :param scene: Original or cleaned ScanSpace scene.
    :type scene: Scene
    :return: Total number of triangular faces.
    :rtype: int
    """
    return sum(
        len(mesh.faces)
        for mesh in _scene_geometry(scene).values()
        if isinstance(mesh, Trimesh)
    )


def _scene_geometry(scene: Scene) -> Mapping[str, object]:
    """Expose the scene's geometry names and check mesh types at use sites.

    :param scene: Imported or cleaned ScanSpace scene.
    :type scene: Scene
    :return: Scene geometry keyed by name.
    :rtype: Mapping[str, object]
    """
    # Trimesh leaves the key and value types of Scene.geometry unspecified.
    return cast(
        Mapping[str, object],
        scene.geometry,  # pyright: ignore[reportUnknownMemberType]
    )
