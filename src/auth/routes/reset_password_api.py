from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.schemas.reset_password_schema import ResetPasswordSchema
from src.auth.services.auth_dependencies import get_current_user
from src.auth.services.reset_password_service import reset_password as reset
from src.core.db import get_session
from src.core.hash_utils import verify_hash
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel

reset_password_router = APIRouter()

@reset_password_router.patch('/reset-password', response_model=ResponseModel)
@limiter.limit("3/1minute")
async def reset_password(
    request : Request,
    schema : ResetPasswordSchema,
    session : AsyncSession = Depends(get_session),
    user : UserAuth = Depends(get_current_user)
):
    result = await reset(session, schema, user)
    response = ResponseModel(
        data=result,
        method=request.method,
        path=request.url.path,
    )
    return response
