"""Encode QR payloads and expose contiguous vector drawing runs."""

from collections.abc import Iterator
from typing import Final

from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.image.pil import PilImage
from qrcode.image.pure import PyPNGImage

QR_QUIET_ZONE_MODULES: Final[int] = 4


def matrix_for(payload: str) -> list[list[bool]]:
    """Encode a payload with medium correction and a quiet zone.

    :param payload: Complete marker payload to encode or print.
    :return: The complete square QR matrix.
    """
    qr: QRCode[PilImage | PyPNGImage] = QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=1,
        border=QR_QUIET_ZONE_MODULES,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    return qr.get_matrix()


def runs_for(
    matrix: list[list[bool]],
) -> Iterator[tuple[int, int, int]]:
    """Yield contiguous black module runs as (x, y, width).

    :param matrix: QR modules including the four-module border.
    :return: Black run coordinates and widths in module units.
    """
    for y, row in enumerate(matrix):
        x: int = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            start: int = x
            while x < len(row) and row[x]:
                x += 1
            yield start, y, x - start
