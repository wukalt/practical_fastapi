from sqlmodel import Session
from typing import Annotated

from fastapi import Depends

from app.core.database import get_session
from app.services.ai import AIService, get_ai_service


SessionDep = Annotated[Session, Depends(get_session)]
AIServiceDep = Annotated[AIService, Depends(get_ai_service)]
