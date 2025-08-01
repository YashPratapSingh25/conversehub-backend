from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.login_schema import LoginSchema
from src.auth.services.login_service import login_user
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

login_router = APIRouter()

@login_router.post('/login', response_model=ResponseModel)
@limiter.limit("3/minute")
async def login(
    request : Request,
    schema : LoginSchema,
    session : AsyncSession = Depends(get_session)
):
    result = await login_user(request, schema, session)
    response = ResponseModel(
        method=request.method,
        data=result,
        message="Login successful",
        path=request.url.path
    )
    return response