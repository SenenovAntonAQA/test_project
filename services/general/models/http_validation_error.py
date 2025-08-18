from typing import Any

from pydantic import BaseModel, ConfigDict


class DetailItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    loc: list[str | int]
    msg: str
    input: Any


class HTTPValidationError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: list[DetailItem]
