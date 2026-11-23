"""Shared strict and immutable Pydantic model."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from src.utils.constants import EXTRA_FORBID


class FrozenModel(BaseModel):
    """Forbid unexpected fields and mutations in user configuration."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra=EXTRA_FORBID, frozen=True
    )
