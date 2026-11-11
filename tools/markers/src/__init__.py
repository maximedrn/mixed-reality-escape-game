"""Generate print-ready spatial QR markers for the escape game."""

from src.config.settings import (
    AVERY_L7160,
    LabelSettings,
    load_markers,
    load_settings,
)
from src.models.entities import Layout, Marker
from src.services.generation import generate
from src.services.pdf import save_pdf
from src.services.qr import matrix_for, runs_for
from src.services.svg import save_svg
from src.utils.validation import parse_grid

__all__: list[str] = [
    "AVERY_L7160",
    "LabelSettings",
    "Layout",
    "Marker",
    "generate",
    "load_markers",
    "load_settings",
    "matrix_for",
    "parse_grid",
    "runs_for",
    "save_pdf",
    "save_svg",
]
