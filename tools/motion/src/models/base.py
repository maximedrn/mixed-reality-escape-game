"""Shared Pydantic model configuration."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from src.utils.constants import (
    FORBID,
)


class FrozenModel(BaseModel):
    """Use immutable models with strict, explicit schema boundaries."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra=FORBID,
        allow_inf_nan=False,
    )
