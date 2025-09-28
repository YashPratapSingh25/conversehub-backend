from fastapi import APIRouter, Depends, HTTPException, Request
from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.services.blob_service import generate_sas_token
from src.core.common_schemas import ResponseModel
from src.core.exceptions_utils.exceptions import ForbiddenError
from src.core.limiter import limiter

sas_token_router = APIRouter()

@sas_token_router.get("/get-sas-token/{user_id}/{session_id}/{turn_id}/{role}", response_model=ResponseModel)
@limiter.limit("1/5min")
async def get_sas_token(
    request : Request,
    user_id : str,
    session_id : str,
    turn_id : str,
    role : str,
    user : UserAuth = Depends(get_current_user)
):
    if str(user.id) != user_id:
        raise ForbiddenError()
    result = await generate_sas_token(user_id=user_id, session_id=session_id, turn_id=turn_id, user=role=="user")
    response = ResponseModel.create_response(request, result)
    return response