from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.auth_dependencies import oauth_scheme
from src.auth.services.refresh_api_service import refresh_api_service as refresh

refresh_router = APIRouter()

@refresh_router.post('/refresh', response_model=ResponseModel)
@limiter.limit("1/10minute")
async def refresh_token(
    request : Request,
    refresh_token : str = Depends(oauth_scheme),
    session : AsyncSession = Depends(get_session)
):
    result = await refresh(request, refresh_token, session)
    response = ResponseModel(
        data=result,
        method=request.method,
        path=request.url.path
    )
    return response