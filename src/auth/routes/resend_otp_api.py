from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.services.otp_service import send_otp
from src.auth.utils.query_pattern import email_pattern
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

resend_otp_router = APIRouter()

@resend_otp_router.post('/resend-email-verification-otp', response_model=ResponseModel)
@limiter.limit("3/minute")
async def resend_otp(
    request : Request,
    tasks : BackgroundTasks,
    email : str = Query(pattern=email_pattern),
    session : AsyncSession = Depends(get_session)
):
    result = await send_otp(email, session, "email_verification", tasks)
    request.state.user = result.get("user_id")
    response = ResponseModel.create_response(data=result, request=request, message="OTP sent")
    return response