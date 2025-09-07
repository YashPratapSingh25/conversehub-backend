from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.services.add_session_service import start_session
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

add_session_router = APIRouter()

@add_session_router.post('/add-session', response_model=ResponseModel)
@limiter.limit("1/minute")
async def add_session(
    request : Request,
    session_name : str = Form(...),
    mode : str = Form("interview"),
    user : UserAuth = Depends(get_current_user),
    resume : UploadFile | None = File(None),
    job_description : str | None = Form(None),
    db_session : AsyncSession = Depends(get_session)
):
    result = await start_session(session_name, user, resume, db_session, job_description, mode)
    response = ResponseModel.create_response(request, result)
    return response