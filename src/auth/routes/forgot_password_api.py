from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.forgot_password_schema import ForgotPasswordSchema
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.auth.services.password_reset_token_service import create_and_store_pwd_reset_token_from_otp as create_reset_token, verify_and_revoke_pwd_reset_token_and_change_password
from src.auth.services.verify_user_service import verify_user
from src.auth.services.otp_service import send_otp, verify_and_revoke_otp
from src.auth.utils.query_pattern import email_pattern
from src.core.common_schemas import ResponseModel
from src.core.db import get_session
from src.core.limiter import limiter

forgot_password_router = APIRouter()

@forgot_password_router.post('/send-forgot-password-otp', response_model=ResponseModel)
@limiter.limit("1/2minute")
async def send_forgot_password_otp(
    request : Request,
    tasks : BackgroundTasks,
    email: str = Query(min_length=3, max_length=320, regex=email_pattern),
    session : AsyncSession = Depends(get_session)
):
    result = await send_otp(email, session, "forgot_password", tasks)
    request.state.user = result.get("user_id")
    response = ResponseModel(
        data=result,
        message="OTP sent",
        method=request.method,
        path=request.url.path,
    )
    return response

@forgot_password_router.post('/verify-forgot-password-otp', response_model=ResponseModel)
@limiter.limit("5/5minute")
async def verify_forgot_password_otp(
    request : Request,
    schema : VerifyOtpSchema,
    session : AsyncSession = Depends(get_session)
):
    result = await create_reset_token(schema, session)
    request.state.user = result.get("user_id")
    response = ResponseModel(
        data=result,
        message="OTP verified",
        method=request.method,
        path=request.url.path
    )
    return response

@forgot_password_router.patch('/forgot-password', response_model=ResponseModel)
@limiter.limit("1/5minute")
async def forgot_password(
    request : Request,
    schema : ForgotPasswordSchema,
    session : AsyncSession = Depends(get_session)
):
    result = await verify_and_revoke_pwd_reset_token_and_change_password(schema, session)
    request.state.user = result.get("user_id")
    response = ResponseModel.create_response(data=result, request=request, message="Password changed successfully")
    return response