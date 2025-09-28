from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.refresh_token_schema import RefreshTokenSchema
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.auth_dependencies import oauth_scheme
from src.auth.services.refresh_api_service import refresh_api_service as refresh

refresh_router = APIRouter()

@refresh_router.post('/refresh', response_model=ResponseModel)
# @limiter.limit("2/1minute")
async def refresh_token(
    request : Request,
    schema : RefreshTokenSchema,
    session : AsyncSession = Depends(get_session)
):
    user_agent = request.headers.get('User-Agent', None)
    ip_address = request.client.host
    result = await refresh(schema, session, user_agent, ip_address)
    request.state.user = result.user_id
    response = ResponseModel.create_response(data=result, request=request)
    return response