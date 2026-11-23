"""Use shared Pydantic settings at application boundaries."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from src.utils.constants import FORBID


class FrozenModel(BaseModel):
    """Use immutable validated models with explicitly controlled fields."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra=FORBID,
        allow_inf_nan=False,
    )
