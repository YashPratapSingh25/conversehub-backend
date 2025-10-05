import os
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.services.turn_orchestrator_service import turn_orchestrator
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

add_turn_router = APIRouter()

@add_turn_router.post('/turn', response_model=ResponseModel)
@limiter.limit("2/minute")
async def add_turn(
    request : Request,
    background_tasks : BackgroundTasks,
    user : UserAuth = Depends(get_current_user),
    db_session : AsyncSession = Depends(get_session),
    audio_file : UploadFile | None = File(None),
    session_id : UUID = Form(...)
):
    result =  await turn_orchestrator(audio_file, session_id, db_session, background_tasks)
    response = ResponseModel.create_response(data=result, request=request)
    return response