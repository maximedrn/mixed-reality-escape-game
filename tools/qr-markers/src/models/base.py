"""Share immutable, finite and explicit Pydantic model configuration."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from src.utils.constants import ALWAYS, FORBID


class FrozenModel(BaseModel):
    """Reject unknown fields and non-finite numbers in immutable models."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra=FORBID,
        allow_inf_nan=False,
        revalidate_instances=ALWAYS,
    )
