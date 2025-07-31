from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.verify_schema import VerifySchema
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.verify_service import verify_user_service as verify

verify_otp_router  = APIRouter()

@verify_otp_router.post('/verify-email-verification-otp', response_model=ResponseModel)
@limiter.limit("5/5minute")
async def verify_email_otp(
    request : Request,
    schema : VerifySchema, 
    session : AsyncSession = Depends(get_session)                       
):
    result = await verify(session, schema)
    response = ResponseModel(
        data=result,
        message="OTP Verified",
        method=request.method,
        path=request.url.path,
    )
    return response