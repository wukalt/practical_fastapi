from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Submission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exercise_id: int | None = Field(default=None, foreign_key="exercise.id")
    code: str = Field(min_length=1, max_length=2400)
    created_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )
