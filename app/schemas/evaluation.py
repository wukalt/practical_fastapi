from pydantic import BaseModel, Field, ConfigDict, PositiveInt, conlist
from pydantic.alias_generators import to_camel


class BaseEvaluation(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_alias=True,
        validate_by_name=True,
        validate_assignment=True
    )


class HintModel(BaseModel):
    text: str = Field(min_length=1, max_length=200)



class EvaluationResponse(BaseEvaluation):
    exercise_id: PositiveInt
    score: int = Field(ge=0, le=100)
    correctness: int = Field(ge=0, le=10)
    functionality: int = Field(ge=0, le=10)

    clean_code: int = Field(ge=0, le=10)
    readability: int = Field(ge=0, le=10)
    maintainability: int = Field(ge=0, le=10)

    feedback: str = Field(min_length=1, max_length=400)
    # hints: list[HintModel] = Field(min_length=1, max_length=5)
    hint : conlist(item_type=HintModel, min_length=1, max_length=5)

