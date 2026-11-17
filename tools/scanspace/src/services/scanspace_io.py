"""Read structural metadata from a ScanSpace ZIP archive."""

from pathlib import Path
from zipfile import ZipFile

from src.models.scanspace import ScanStructure
from src.utils.constants import STRUCTURE_JSON_PATH


def load_structure(path: Path) -> ScanStructure:
    """Load and validate RoomPlan structure information from a ZIP archive.

    :param path: ScanSpace container with room/structure.json.
    :type path: Path
    :return: Validated window definitions and dimensions.
    :rtype: ScanStructure
    """
    with ZipFile(path) as archive:
        return ScanStructure.model_validate_json(
            archive.read(STRUCTURE_JSON_PATH)
        )
