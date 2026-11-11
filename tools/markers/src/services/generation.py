"""Coordinate TOML loading and SVG, CSV and PDF exports."""

from pathlib import Path
from tomllib import load

from src.config.settings import LabelSettings, load_markers, load_settings
from src.models.configuration import MarkerConfig
from src.models.entities import Marker
from src.services.manifest import save_manifest
from src.services.pdf import save_pdf
from src.services.qr import matrix_for
from src.services.svg import save_svg
from src.utils.constants import (
    MANIFEST_FILENAME,
    PDF_FILENAME,
    READ_BINARY_MODE,
    SVG_DIRECTORY,
)


def generate(
    config_path: Path,
    output: Path | None = None,
    grid: tuple[int, int] | None = None,
) -> tuple[int, Path]:
    """Export every configured marker as SVG, CSV and PDF.

    :param config_path: Source TOML configuration path.
    :param output: Optional export directory override.
    :param grid: Optional column and row override.
    :return: The marker count and export directory.
    """
    with config_path.open(READ_BINARY_MODE) as file:
        data: MarkerConfig = MarkerConfig.model_validate(load(file))

    markers: list[Marker] = load_markers(data)
    settings: LabelSettings = load_settings(data, grid)
    svg_size_mm: float = data.output.svg_size_mm
    output_name: str = data.output.directory
    destination: Path = (
        output if output is not None else config_path.parent / output_name
    )
    svg_dir: Path = destination / SVG_DIRECTORY
    svg_dir.mkdir(parents=True, exist_ok=True)

    for marker in markers:
        save_svg(
            matrix_for(marker.payload),
            svg_size_mm,
            svg_dir / marker.filename,
            marker.payload,
        )
    save_manifest(markers, destination / MANIFEST_FILENAME)
    save_pdf(markers, settings, destination / PDF_FILENAME)
    return len(markers), destination
