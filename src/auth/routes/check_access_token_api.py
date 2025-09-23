from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.schemas.refresh_token_schema import RefreshTokenSchema
from src.auth.services.refresh_token_service import verify_and_revoke_refresh_token as logout_refresh_token
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.auth_dependencies import get_current_user, oauth_scheme

check_access_token_router = APIRouter()

@check_access_token_router.get('/check-access-token', response_model=ResponseModel)
@limiter.limit("1/2minute")
async def check_access_token(
    request : Request,
    user : UserAuth = Depends(get_current_user),
):
    response = ResponseModel.create_response(data={}, request=request)
    return response