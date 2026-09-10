from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel


class BaseExercise(BaseModel):
    model_config = ConfigDict(
        alias_generator= to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        validate_assignment=True
    )



class ExerciseRequest(BaseExercise):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=800)


class ExerciseResponse(ExerciseRequest):
    id: int
    created_at: datetime

    @field_serializer('created_at', when_used='json')
    def serialize_date_time(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H-%M-%S")



class ExerciseUpdate(BaseExercise):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, min_length=1, max_length=800)
