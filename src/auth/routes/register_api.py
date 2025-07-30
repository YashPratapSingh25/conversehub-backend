from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.register_schema import RegisterSchema
from src.auth.services.register_service import register
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

register_router = APIRouter()

@register_router.post('/register', response_model=ResponseModel)
@limiter.limit("5/minute")
async def register_user(
    request : Request,
    schema : RegisterSchema,
    session : AsyncSession = Depends(get_session)
):  
    result = await register(schema=schema, session = session)
    response = ResponseModel(
        method=request.method,
        path=request.url.path,
        message="User created successfully",
        status_code=201,
        data=result    
    )
    return response