from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.services.resend_otp_service import resend_otp as resend
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter
from src.core.constants import constants

resend_otp_router = APIRouter()

@resend_otp_router.post('/resend-email-verification-otp', response_model=ResponseModel)
@limiter.limit("3/minute")
async def resend_otp(
    request : Request,
    tasks : BackgroundTasks,
    email : EmailStr = Query(),
    session : AsyncSession = Depends(get_session)
):
    result = await resend(email, session, constants.EmailVerificationUsage, tasks)
    response = ResponseModel(
        data=result,
        message="OTP sent",
        method=request.method,
        path=request.url.path,
    )
    return response