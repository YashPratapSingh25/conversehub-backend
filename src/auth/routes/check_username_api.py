from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.services.check_username_service import check_username_exists as check
from src.auth.utils.query_pattern import username_pattern
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel

check_username_router = APIRouter()

@check_username_router.get('/check-username-exists', response_model=ResponseModel)
@limiter.limit("10/minute")
async def check_username(
    request : Request,
    username : str = Query(min_length=3, max_length=20, pattern=username_pattern),
    session : AsyncSession = Depends(get_session),
):
    result = await check(username, session)
    response = ResponseModel(
        data=result,
        method=request.method,
        path=request.url.path
    )
    return response