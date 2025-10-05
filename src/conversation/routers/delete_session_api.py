from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.services.auth_dependencies import get_current_user
from src.conversation.schemas.delete_session_schema import DeleteSessionSchema
from src.conversation.services.delete_session_service import delete_session_service
from src.core.common_schemas import ResponseModel
from src.core.db import get_session

delete_session_router = APIRouter()

@delete_session_router.delete('/session', response_model=ResponseModel)
async def delete_session(
    request : Request,
    delete_session_schema : DeleteSessionSchema,
    db_session : AsyncSession = Depends(get_session),
    user : UserAuth = Depends(get_current_user)
):
    await delete_session_service(db_session, delete_session_schema)
    response = ResponseModel.create_response(request, {})
    return response