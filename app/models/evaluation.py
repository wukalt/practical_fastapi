from datetime import datetime, timezone
from sqlmodel import SQLModel, Field



class Evaluation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_id : int | None = Field(default=None, foreign_key='exercise.id')

    score: int = Field(ge=0, le=100)
    correctness: int = Field(ge=0, le=10)
    functionality: int = Field(ge=0, le=10)

    clean_code: int = Field(ge=0, le=10)
    readability: int = Field(ge=0, le=10)
    maintainability: int = Field(ge=0, le=10)

    created_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )
