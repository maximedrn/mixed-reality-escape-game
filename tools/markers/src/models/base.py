"""Share immutable, finite and explicit Pydantic model configuration."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from src.utils.constants import ALWAYS, FORBID


class FrozenModel(BaseModel):
    """Validate defaults and reject unknown fields and non-finite numbers."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra=FORBID,
        validate_default=True,
        allow_inf_nan=False,
        revalidate_instances=ALWAYS,
    )
