import os
from fastapi import APIRouter, Depends, File, Request, UploadFile

from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.services.orchestrator_service import orchestrator
from src.core.common_schemas import ResponseModel
from src.core.limiter import limiter

add_turn_router = APIRouter()

@add_turn_router.post('/add-turn', response_model=ResponseModel)
@limiter.limit("2/minute")
async def add_turn(
    request : Request,
    user : UserAuth = Depends(get_current_user),
    audio_file : UploadFile = File(...)
):
    result =  await orchestrator(audio_file)
    response = ResponseModel.create_response(data=result, request=request)
    return response