from pydantic import BaseModel, ConfigDict, Field

from services.university.models.base_grade import BaseGrade


class GradeResponse(BaseGrade):
    id: int


class GradeStatisticResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=0)
    min: int | None = Field(..., ge=0, le=5)
    max: int | None = Field(..., ge=0, le=5)
    avg: float | None = Field(..., ge=0, le=5)
