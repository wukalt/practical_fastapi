from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_serializer, FieldSerializationInfo

from pydantic.alias_generators import to_camel



class BaseSubmission(BaseModel):
    model_config = ConfigDict(
        alias_generator= to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        validate_assignment=True
    )


class SubmissionRequest(BaseSubmission):
    exercise_id: int
    code: str = Field(min_length=1, max_length=2400)


class SubmissionResponse(SubmissionRequest):
    id: int
    created_at: datetime

    @field_serializer('created_at', when_used='json')
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H-%M-%S")


class SubmissionUpdate(BaseModel):
    code: str | None
