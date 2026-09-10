from typing import Annotated
from sqlmodel import select
from fastapi import APIRouter, status, Body, Path, HTTPException

from app.dependencies import SessionDep
from app.models.exercise import Exercise
from app.schemas.exercise import (
    ExerciseRequest,
    ExerciseResponse,
    ExerciseUpdate
)

router = APIRouter(
    prefix='/api/v1/exercises',
    tags=['exercises', 'v1']
)


NotFoundException = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="The exercise is not found"
)


@router.get(
    '/',
    response_model=list[ExerciseResponse]
)
async def get_all_exercises(
    session: SessionDep
) -> list[ExerciseResponse]:
    return session.exec(select(Exercise)).all()



@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def post_exercise(
    exercise: Annotated[ExerciseRequest, Body()],
    session: SessionDep
) -> None:
    exercise_db = Exercise.model_validate(exercise)
    session.add(exercise_db)
    session.commit()
    session.refresh(exercise_db)



@router.patch(
    '/{id:int}/update',
    response_model=ExerciseResponse
)
async def update_exercise(
    id: Annotated[int, Path()],
    exercise: Annotated[ExerciseUpdate, Body()],
    session: SessionDep
) -> ExerciseResponse:
    exercise_db = session.exec(
        select(Exercise).where(Exercise.id == id)
    ).first()

    if not exercise_db:
        raise NotFoundException

    exercise_db.sqlmodel_update(
        exercise.model_dump(exclude_unset=True)
    )

    session.add(exercise_db)
    session.commit()
    session.refresh(exercise_db)
    
    return exercise_db



@router.delete(
    '/{id:int}/delete',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_exercise(
    id: Annotated[int, Path()],
    session: SessionDep
) -> None:
    exercise_db = session.exec(
        select(Exercise).where(Exercise.id == id)
    ).first()

    if not exercise_db:
        raise NotFoundException

    session.delete(exercise_db)
    session.commit()
