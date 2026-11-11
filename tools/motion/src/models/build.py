"""Validate filesystem inputs and the animated GLB destination."""

from pathlib import Path
from typing import Self

from pydantic import FilePath, model_validator

from src.models.base import FrozenModel
from src.utils.constants import GLB_SUFFIX
from src.utils.messages import (
    BUILD_DESTINATIONS_ERROR,
    OUTPUT_GLB_SUFFIX_ERROR,
)


class BuildRequest(FrozenModel):
    """Require existing inputs and distinct destinations before any export."""

    model: FilePath
    animation: FilePath
    output_glb: Path

    @model_validator(mode="after")
    def validate_destinations(self) -> Self:
        """Protect inputs from destinations that resolve to the same file.

        :return: The validated build request.
        :rtype: Self
        """
        sources: set[Path] = {
            path.resolve() for path in (self.model, self.animation)
        }
        glb: Path = self.output_glb.resolve()
        if glb in sources:
            raise ValueError(BUILD_DESTINATIONS_ERROR)
        if glb.suffix.lower() != GLB_SUFFIX:
            raise ValueError(OUTPUT_GLB_SUFFIX_ERROR)
        return self


class BuildResult(FrozenModel):
    """Return only output files that actually exist after publication."""

    glb: FilePath
