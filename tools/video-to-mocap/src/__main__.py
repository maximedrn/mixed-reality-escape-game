"""Run the project as a Python module."""

from src.cli import main
from src.utils.constants import ENTRYPOINT_NAME

if __name__ == ENTRYPOINT_NAME:
    main()
