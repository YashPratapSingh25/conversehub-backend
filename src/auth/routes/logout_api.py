from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
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
    refresh_token : str = Depends(oauth_scheme),
    session : AsyncSession = Depends(get_session)   
):
    await logout_refresh_token(complete_token=refresh_token, session=session)
    response = ResponseModel(
        data={},
        message="Logout successful",
        status_code=200,
        path=request.base_url.path,
        method=request.method
    )
    return response