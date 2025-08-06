from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.auth.services.verify_user_service import verify_user

verify_otp_router  = APIRouter()

@verify_otp_router.post('/verify-email-verification-otp', response_model=ResponseModel)
@limiter.limit("5/5minute")
async def verify_user_with_otp(
    request : Request,
    schema : VerifyOtpSchema, 
    session : AsyncSession = Depends(get_session)                       
):
    result = await verify_user(session, schema)
    response = ResponseModel.create_response(data=result, request=request, message="OTP Verified")
    return response