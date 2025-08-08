from pydantic import BaseModel, ConfigDict, Field

from services.university.models.base_grade import BaseGrade


class GradeResponse(BaseGrade):
    id: int


class GradeStatisticResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int = Field(ge=0)
    min: int = Field(..., ge=0, le=5, description="оценки от 0 до 5") | None
    max: int = Field(..., ge=0, le=5, description="оценки от 0 до 5") | None
    avg: int = Field(..., ge=0, le=5, description="оценки от 0 до 5") | None
