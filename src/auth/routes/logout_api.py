from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.refresh_token_schema import RefreshTokenSchema
from src.auth.services.refresh_token_service import verify_and_revoke_refresh_token as logout_refresh_token
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.auth_dependencies import oauth_scheme

logout_router = APIRouter()

@logout_router.post('/logout', response_model=ResponseModel)
@limiter.limit("1/2minute")
async def logout(
    request : Request,
    schema : RefreshTokenSchema,
    session : AsyncSession = Depends(get_session)   
):
    result = await logout_refresh_token(complete_token=schema.refresh_token, session=session)
    request.state.user = result.user_id
    response = ResponseModel.create_response(data={}, request=request, message="Logout successful")
    return response