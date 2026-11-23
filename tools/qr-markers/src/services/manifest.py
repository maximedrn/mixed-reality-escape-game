"""Export the marker-to-object mapping as a UTF-8 CSV manifest."""

from csv import writer
from pathlib import Path

from src.models.entities import Marker
from src.utils.constants import (
    EMPTY_TEXT,
    MANIFEST_COLUMNS,
    MANIFEST_SVG_TEMPLATE,
    SVG_DIRECTORY,
    TEXT_ENCODING,
    WRITE_TEXT_MODE,
)


def save_manifest(markers: list[Marker], path: Path) -> None:
    """Write marker identifiers, complete payloads and relative SVG paths.

    :param markers: Marker identities in configuration order.
    :param path: Destination CSV file.
    """
    rows: list[list[str]] = [list(MANIFEST_COLUMNS)]
    rows.extend(
        [
            marker.game_id,
            marker.room_id,
            marker.object_id,
            marker.payload,
            MANIFEST_SVG_TEMPLATE.format(
                directory=SVG_DIRECTORY, filename=marker.filename
            ),
        ]
        for marker in markers
    )
    with path.open(
        WRITE_TEXT_MODE, encoding=TEXT_ENCODING, newline=EMPTY_TEXT
    ) as file:
        writer(file).writerows(rows)
