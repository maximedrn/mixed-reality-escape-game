"""Lay out vector QR codes and readable identifiers on PDF sheets."""

from pathlib import Path
from typing import Final

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

from src.config.settings import LabelSettings
from src.models.entities import Layout, Marker
from src.services.qr import matrix_for, runs_for
from src.utils.constants import (
    BLACK_HEX,
    CENTER_DIVISOR,
    ELLIPSIS,
    FONT_NAME,
    LIGHT_GRAY_HEX,
    PADDING_SIDES,
    PDF_AUTHOR,
    PDF_TITLE,
)

BLACK: Final[Color] = HexColor(BLACK_HEX)
LIGHT_GRAY: Final[Color] = HexColor(LIGHT_GRAY_HEX)


MIN_FITTED_FONT_PT: Final[float] = 4.0
FONT_STEP_PT: Final[float] = 0.25
GUIDE_LINE_WIDTH_PT: Final[float] = 0.35
MIN_CAPTION_BAND_MM: Final[float] = 3.0
MAX_CAPTION_FONT_PT: Final[float] = 14.0
MIN_CAPTION_FONT_PT: Final[float] = 7.0
CAPTION_FONT_SCALE: Final[float] = 0.14
CAPTION_WIDTH_FRACTION: Final[float] = 0.97
CAPTION_BASELINE_OFFSET_MM: Final[float] = 0.15
MIN_SIDE_TEXT_WIDTH_MM: Final[float] = 11.0
GAME_LINE_OFFSET_PT: Final[float] = 10.0
OBJECT_LINE_OFFSET_PT: Final[float] = 11.0
GAME_FONT_SIZE_PT: Final[float] = 7.0
SIDE_FONT_SIZE_PT: Final[float] = 8.0


def draw_qr(
    pdf: Canvas,
    matrix: list[list[bool]],
    x_mm: float,
    y_mm: float,
    size_mm: float,
) -> None:
    """Draw a QR matrix as contiguous vector rectangles on a PDF.

    :param pdf: Canvas receiving the vector output.
    :param matrix: QR modules including the four-module border.
    :param x_mm: Left coordinate in millimeters.
    :param y_mm: Bottom coordinate in millimeters.
    :param size_mm: Physical QR width in millimeters.
    """
    modules: int = len(matrix)
    step: float = size_mm * mm / modules
    x: float = x_mm * mm
    y: float = y_mm * mm
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(x, y, size_mm * mm, size_mm * mm, stroke=0, fill=1)
    pdf.setFillColor(BLACK)
    for col, row, width in runs_for(matrix):
        pdf.rect(
            x + col * step,
            y + (modules - row - 1) * step,
            width * step,
            step,
            stroke=0,
            fill=1,
        )


def draw_fitted_text(
    pdf: Canvas,
    text: str,
    x_pt: float,
    y_pt: float,
    available_pt: float,
    preferred_pt: float,
) -> None:
    """Fit readable identification text within the label width.

    :param pdf: Canvas receiving the vector output.
    :param text: Readable identifier to draw.
    :param x_pt: Left coordinate in PDF points.
    :param y_pt: Baseline coordinate in PDF points.
    :param available_pt: Available text width in PDF points.
    :param preferred_pt: Preferred font size in PDF points.
    """
    size: float = preferred_pt
    while (
        size > MIN_FITTED_FONT_PT
        and stringWidth(text, FONT_NAME, size) > available_pt
    ):
        size -= FONT_STEP_PT
    if stringWidth(text, FONT_NAME, size) > available_pt:
        # The QR retains the complete ID; never draw outside the label.
        while (
            text
            and stringWidth(text + ELLIPSIS, FONT_NAME, size) > available_pt
        ):
            text = text[:-1]
        text += ELLIPSIS
    pdf.setFont(FONT_NAME, size)
    pdf.drawString(x_pt, y_pt, text)


def draw_label(
    pdf: Canvas,
    marker: Marker,
    matrix: list[list[bool]],
    col: int,
    row: int,
    settings: LabelSettings,
) -> None:
    """Draw one marker and its identifiers in a sheet position.

    :param pdf: Canvas receiving the vector output.
    :param marker: Marker identity to print.
    :param matrix: QR modules including the four-module border.
    :param col: Zero-based label column.
    :param row: Zero-based label row.
    :param settings: Validated label and printer settings.
    """
    layout: Layout = settings.layout
    left: float = (
        layout.margin_left_mm
        + col * (layout.label_width_mm + layout.gap_x_mm)
        + settings.shift_x_mm
    )
    top: float = (
        layout.margin_top_mm
        + row * (layout.label_height_mm + layout.gap_y_mm)
        + settings.shift_y_mm
    )
    bottom: float = layout.page_height_mm - top - layout.label_height_mm

    if settings.draw_guides:
        pdf.setStrokeColor(LIGHT_GRAY)
        pdf.setLineWidth(GUIDE_LINE_WIDTH_PT)
        pdf.rect(
            left * mm,
            bottom * mm,
            layout.label_width_mm * mm,
            layout.label_height_mm * mm,
            stroke=1,
            fill=0,
        )

    qr_x: float = left + settings.padding_mm
    available_band_mm: float = (
        layout.label_height_mm
        - settings.qr_size_mm
        - PADDING_SIDES * settings.padding_mm
    )
    has_caption: bool = (
        settings.show_text and available_band_mm >= MIN_CAPTION_BAND_MM
    )
    font_size: float = 0.0
    group_bottom: float = bottom
    if has_caption:
        font_size = min(
            MAX_CAPTION_FONT_PT,
            max(MIN_CAPTION_FONT_PT, settings.qr_size_mm * CAPTION_FONT_SCALE),
            (available_band_mm - 1.0) * mm,
            settings.qr_size_mm
            * mm
            * CAPTION_WIDTH_FRACTION
            / stringWidth(marker.payload, FONT_NAME, 1),
        )
        caption_band_mm: float = 1.0 + font_size / mm
        group_bottom = (
            bottom
            + (layout.label_height_mm - settings.qr_size_mm - caption_band_mm)
            / CENTER_DIVISOR
        )
        qr_y: float = group_bottom + caption_band_mm
    else:
        qr_y = (
            bottom
            + (layout.label_height_mm - settings.qr_size_mm) / CENTER_DIVISOR
        )
    draw_qr(pdf, matrix, qr_x, qr_y, settings.qr_size_mm)

    if not settings.show_text:
        return
    if has_caption:
        # Keep the ID immediately below the QR on both small and large sheets.
        pdf.setFillColor(BLACK)
        pdf.setFont(FONT_NAME, font_size)
        pdf.drawCentredString(
            (qr_x + settings.qr_size_mm / CENTER_DIVISOR) * mm,
            (group_bottom + CAPTION_BASELINE_OFFSET_MM) * mm,
            marker.payload,
        )
    text_x: float = qr_x + settings.qr_size_mm + settings.padding_mm
    text_width: float = (
        left + layout.label_width_mm - settings.padding_mm - text_x
    ) * mm
    if text_width < MIN_SIDE_TEXT_WIDTH_MM * mm:
        return

    pdf.setFillColor(BLACK)
    label_middle: float = (
        bottom + layout.label_height_mm / CENTER_DIVISOR
    ) * mm
    draw_fitted_text(
        pdf,
        marker.game_id,
        text_x * mm,
        label_middle + GAME_LINE_OFFSET_PT,
        text_width,
        GAME_FONT_SIZE_PT,
    )
    draw_fitted_text(
        pdf,
        marker.room_id,
        text_x * mm,
        label_middle,
        text_width,
        SIDE_FONT_SIZE_PT,
    )
    draw_fitted_text(
        pdf,
        marker.object_id,
        text_x * mm,
        label_middle - OBJECT_LINE_OFFSET_PT,
        text_width,
        SIDE_FONT_SIZE_PT,
    )


def save_pdf(
    markers: list[Marker], settings: LabelSettings, path: Path
) -> None:
    """Paginate vector QR markers onto printable label sheets.

    :param markers: Marker identities in print order.
    :param settings: Validated label and printer settings.
    :param path: Destination file path.
    """
    layout: Layout = settings.layout
    pdf: Canvas = Canvas(
        str(path),
        pagesize=(layout.page_width_mm * mm, layout.page_height_mm * mm),
        pageCompression=1,
    )
    pdf.setTitle(PDF_TITLE)
    pdf.setAuthor(PDF_AUTHOR)

    page_index: int = -1
    for index, marker in enumerate(markers):
        absolute_slot: int = settings.start_index + index
        target_page: int
        slot: int
        target_page, slot = divmod(absolute_slot, layout.capacity)
        if target_page != page_index:
            if page_index != -1:
                pdf.showPage()
            page_index = target_page
        col: int
        row: int
        col, row = slot % layout.columns, slot // layout.columns
        draw_label(pdf, marker, matrix_for(marker.payload), col, row, settings)

    pdf.save()
