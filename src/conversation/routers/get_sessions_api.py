from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.services.get_sessions_service import get_sessions
from src.core.db import get_session
from src.core.common_schemas import ResponseModel
from src.core.limiter import limiter

get_sessions_router = APIRouter()

@get_sessions_router.get('/sessions', response_model=ResponseModel)
async def get_session(
    request : Request,
    limit : int = Query(3, ge=1, le=10),
    offset : int = Query(0, ge=0),
    db_session : AsyncSession = Depends(get_session),
    user : UserAuth = Depends(get_current_user)
):  
    result = await get_sessions(limit, offset, db_session, user)
    response = ResponseModel.create_response(request, result)
    return response