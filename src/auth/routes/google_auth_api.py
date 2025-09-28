from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import httpx
from src.auth.schemas.google_auth_schema import GoogleAuthSchema
from src.auth.services.google_auth_service import auth_with_google
from src.core.common_schemas import ResponseModel
from src.core.config import settings
from src.core.db import get_session
from src.core.limiter import limiter

google_auth_router = APIRouter()

@google_auth_router.post("/google", response_model=ResponseModel)
# @limiter.limit("2/1min")
async def google_auth(
    request : Request,
    schema : GoogleAuthSchema,
    session : AsyncSession = Depends(get_session),
):
    result = await auth_with_google(request, schema, session)
    request.state.user = result.user_id
    response = ResponseModel.create_response(request, result)
    return response