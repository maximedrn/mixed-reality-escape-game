"""Retain architectural meshes and cover ScanSpace window openings."""

from pathlib import Path

import numpy as np
import trimesh
from numpy import float64
from numpy.typing import NDArray
from trimesh import Scene, Trimesh
from trimesh.visual import TextureVisuals

from src.config.defaults import (
    FIRST_WINDOW_INDEX,
    TRANSFORM_SIDE,
    WINDOW_OVERLAP_M,
    WINDOW_PATCH_DEPTH_M,
)
from src.models.arguments import CleanArguments
from src.models.result import CleanResult
from src.models.scanspace import ScanStructure, WindowDefinition
from src.services.scanspace_io import load_structure
from src.utils.constants import (
    ARCHITECTURE_MESHES,
    GLB_SUFFIX,
    SCENE_FORMAT,
    WALL_GEOMETRY_NAME,
    WINDOW_NAME_TEMPLATE,
)
from src.utils.messages import (
    INVALID_MESH_ERROR,
    INVALID_SCENE_ERROR,
    MATERIAL_REQUIRED_ERROR,
    OUTPUT_OVERLAPS_INPUT_ERROR,
    OUTPUT_SUFFIX_ERROR,
)


def clean_architecture(options: CleanArguments) -> CleanResult:
    """Publish a floorplan stripped of furniture and filled at its windows.

    :param options: Existing GLB/ScanSpace input paths and output GLB path.
    :type options: CleanArguments
    :return: Output path, mesh counts, and resulting scene bounds.
    :rtype: CleanResult
    """
    source_file: Path = options.input.expanduser().resolve()
    scan_file: Path = options.scan.expanduser().resolve()
    output_file: Path = options.output.expanduser().resolve()
    if output_file.suffix.lower() != GLB_SUFFIX:
        raise ValueError(OUTPUT_SUFFIX_ERROR)
    if output_file in (source_file, scan_file):
        raise ValueError(OUTPUT_OVERLAPS_INPUT_ERROR)

    structure: ScanStructure = load_structure(scan_file)
    original = trimesh.load(source_file, force=SCENE_FORMAT)
    if not isinstance(original, Scene):
        raise ValueError(INVALID_SCENE_ERROR)
    cleaned: Scene = _retain_architecture(original)
    for index, window in enumerate(
        structure.windows, start=FIRST_WINDOW_INDEX
    ):
        patch: Trimesh = _window_patch(original, window)
        name: str = WINDOW_NAME_TEMPLATE.format(index=index)
        cleaned.add_geometry(patch, geom_name=name, node_name=name)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned.export(output_file)
    bounds: NDArray[float64] = np.asarray(cleaned.bounds, dtype=float64)
    return CleanResult(
        output=output_file,
        original_faces=_face_count(original),
        clean_faces=_face_count(cleaned),
        windows_filled=len(structure.windows),
        bounds=bounds.tolist(),
        geometry={
            name: len(mesh.faces)
            for name, mesh in cleaned.geometry.items()
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
        cleaned.add_geometry(
            geometry.copy(), geom_name=name, node_name=name
        )
    return cleaned


def _window_patch(original: Scene, window: WindowDefinition) -> Trimesh:
    """Produce a textured wall slab at one RoomPlan window transform.

    :param original: Original scene containing the wall texture.
    :type original: Scene
    :param window: Width, height and column-major world transform.
    :type window: WindowDefinition
    :return: Window-filling mesh using the source wall material.
    :rtype: Trimesh
    """
    wall: Trimesh = _mesh(original, WALL_GEOMETRY_NAME)
    if not isinstance(wall.visual, TextureVisuals):
        raise ValueError(MATERIAL_REQUIRED_ERROR)
    transform: NDArray[float64] = np.asarray(
        window.transform, dtype=float64
    ).reshape((TRANSFORM_SIDE, TRANSFORM_SIDE)).T
    width, height, _ = window.dimensions
    patch: Trimesh = trimesh.creation.box(
        extents=[
            width + WINDOW_OVERLAP_M,
            height + WINDOW_OVERLAP_M,
            WINDOW_PATCH_DEPTH_M,
        ]
    )
    vertices: NDArray[float64] = np.asarray(patch.vertices, dtype=float64)
    uv: NDArray[float64] = np.column_stack(
        (vertices[:, 0], vertices[:, 1])
    )
    patch.visual = TextureVisuals(uv=uv, material=wall.visual.material)
    patch.apply_transform(transform)
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
    value: object = scene.geometry.get(name)
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
        for mesh in scene.geometry.values()
        if isinstance(mesh, Trimesh)
    )
