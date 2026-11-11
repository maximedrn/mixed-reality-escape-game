"""Export QR matrices and complete marker captions as vector SVG."""

from pathlib import Path
from typing import Final
from xml.sax.saxutils import escape

from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

from src.services.qr import runs_for
from src.utils.constants import (
    CENTER_DIVISOR,
    FONT_NAME,
    SPACE,
    SVG_DOCUMENT_TEMPLATE,
    SVG_PATH_SEGMENT_TEMPLATE,
    TEXT_ENCODING,
)
from src.utils.messages import SVG_PAYLOAD_ERROR, SVG_SIZE_ERROR

MAX_CAPTION_FONT_PT: Final[float] = 20.0
MIN_CAPTION_FONT_PT: Final[float] = 7.0
CAPTION_FONT_SCALE: Final[float] = 0.23
CAPTION_GAP_SCALE: Final[float] = 0.015
CAPTION_DESCENT_MM: Final[float] = 0.8
CAPTION_BASELINE_FRACTION: Final[float] = 0.8


def svg_caption_size_pt(payload: str, qr_size_mm: float) -> float:
    """Select a caption font size that fits beneath the QR code.

    :param payload: Complete marker payload to encode or print.
    :param qr_size_mm: QR width including the quiet zone.
    :return: Caption font size in PDF points.
    """
    available_width: float = (qr_size_mm - 1.0) * mm
    width_at_one_point: float = stringWidth(payload, FONT_NAME, 1)
    return min(
        MAX_CAPTION_FONT_PT,
        max(MIN_CAPTION_FONT_PT, qr_size_mm * CAPTION_FONT_SCALE),
        available_width / width_at_one_point,
    )


def save_svg(
    matrix: list[list[bool]], size_mm: float, path: Path, payload: str
) -> None:
    """Write a vector QR and its exact payload underneath in one SVG.

    :param matrix: QR modules including the four-module border.
    :param size_mm: Physical QR width in millimeters.
    :param path: Destination file path.
    :param payload: Complete marker payload to encode or print.
    :raises ValueError: If the supplied values are invalid.
    """
    if size_mm <= 0:
        raise ValueError(SVG_SIZE_ERROR)
    if not payload:
        raise ValueError(SVG_PAYLOAD_ERROR)

    modules: int = len(matrix)
    segments: list[str] = [
        SVG_PATH_SEGMENT_TEMPLATE.format(x=x, y=y, width=width)
        for x, y, width in runs_for(matrix)
    ]
    font_size_mm: float = svg_caption_size_pt(payload, size_mm) / mm
    caption_gap_mm: float = max(1.0, size_mm * CAPTION_GAP_SCALE)
    caption_height_mm: float = (
        caption_gap_mm + font_size_mm + CAPTION_DESCENT_MM
    )
    total_height_mm: float = size_mm + caption_height_mm
    baseline_mm: float = (
        size_mm + caption_gap_mm + CAPTION_BASELINE_FRACTION * font_size_mm
    )
    scale: float = size_mm / modules
    safe_payload: str = escape(payload)

    content: str = SVG_DOCUMENT_TEMPLATE.format(
        size_mm=size_mm,
        total_height_mm=total_height_mm,
        safe_payload=safe_payload,
        scale=scale,
        segments=SPACE.join(segments),
        center_mm=size_mm / CENTER_DIVISOR,
        baseline_mm=baseline_mm,
        font_size_mm=font_size_mm,
    )
    path.write_text(content, encoding=TEXT_ENCODING)
