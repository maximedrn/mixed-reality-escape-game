"""Resolve project-relative paths and TOML configuration."""

from pathlib import Path
from tomllib import loads

from src.models.configuration import ProjectConfig
from src.utils.constants import (
    TEXT_ENCODING,
)


def load_config(file: Path) -> ProjectConfig:
    """Parse a project's TOML configuration with Pydantic validation.

    :param file: Configuration file with UTF-8 encoded TOML.
    :type file: Path
    :return: Validated project configuration.
    :rtype: ProjectConfig
    """
    return ProjectConfig.model_validate(loads(file.read_text(TEXT_ENCODING)))


def project_path(config_file: Path, value: Path) -> Path:
    """Resolve paths relative to the TOML file's parent directory.

    :param config_file: Configuration file defining the base directory.
    :type config_file: Path
    :param value: Configured absolute, relative or user-home path.
    :type value: Path
    :return: A path independent of the process working directory.
    :rtype: Path
    """
    value = value.expanduser()
    if value.is_absolute():
        return value
    return config_file.resolve().parent / value
