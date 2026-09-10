from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class Exercise(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=800)
    created_at: datetime = Field(
        default_factory=lambda: 
            datetime.now(timezone.utc)
    )
