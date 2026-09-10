import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.api.routers.v1 import (
    submission,
    exercise,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.http_client = httpx.AsyncClient(
        base_url="https://api.groq.com",
        timeout=30.0,
    )

    yield

    await app.state.http_client.aclose()


app = FastAPI(
    lifespan=lifespan,
)

create_db_and_tables()


app.include_router(submission.router)
app.include_router(exercise.router)



