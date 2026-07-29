from typing import Literal

from local_fc.models.camel_case_model import CamelCaseModel


class HealthResponse(CamelCaseModel):
    """Health response model."""

    status: Literal["ok"] = "ok"
