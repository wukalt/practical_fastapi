import httpx
from app.schemas.evaluation import EvaluationResponse
from typing import Annotated
from sqlmodel import select
from fastapi import APIRouter, Body, status, Path, HTTPException

from app.dependencies import SessionDep, AIServiceDep
from app.models.submission import Submission
from app.models.exercise import Exercise
from app.schemas.submission import (
    SubmissionRequest,
    SubmissionResponse,
    SubmissionUpdate
)


router = APIRouter(
    prefix='/api/v1/submissions',
    tags=['submissions', 'v1']
)

NotFoundHTTPException= HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail=f"Submission is not found"
)


@router.get(
    '/',
    response_model=list[SubmissionResponse]
)
async def get_all_submissions(
    session: SessionDep
):
    return session.exec(select(Submission)).all()



@router.post(
    "/",
    response_model=EvaluationResponse
)
async def send_submission(
    submission: Annotated[SubmissionRequest, Body()],
    session: SessionDep,
    ai_service: AIServiceDep,
):
    exercise_db= session.exec(
        select(Exercise).where(Exercise.id == submission.exercise_id)
    ).first()

    if not exercise_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no exercise found.",
        )

    try:
        result = await ai_service.evaluate(
            exercise=exercise_db.description,
            code=submission.code,
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ارتباط با سرویس ارزیابی برقرار نشد.",
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="خطا در سرویس ارزیابی کد.",
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="پاسخ نامعتبر از سرویس ارزیابی دریافت شد.",
        )
    return result


@router.patch(
    '/{id:int}/update',
    response_model=SubmissionResponse
)
async def update_submission(
    id: Annotated[int, Path()],
    submission: Annotated[SubmissionUpdate, Body()],
    session: SessionDep
):
    submission_db = session.exec(select(Submission).where(Submission.id == id)).first()
    if not submission_db:
        raise NotFoundHTTPException
    submission_db.sqlmodel_update(
        submission.model_dump(exclude_unset=True)
    )
    session.add(submission_db)
    session.commit()
    session.refresh(submission_db)

    return submission_db



@router.delete(
    '/{id:int}/delete',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_submission(
    id: Annotated[int, Path()],
    session: SessionDep
) -> None:
    submission_db = session.exec(select(Submission).where(
        Submission.id == id
    )).first()

    if not submission_db:
        raise NotFoundHTTPException

    session.delete(submission_db)
    session.commit()
