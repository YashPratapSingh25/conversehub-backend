from fastapi import BackgroundTasks
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.user_response_schema import UserResponseModel
from src.auth.services.otp_service import create_otp
from src.auth.services.get_user_by_email_service import get_user_by_email
from src.core.emails.mail_utils import send_otp_mail
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.constants import constants

async def resend_otp(email : str, session : AsyncSession, usage : str, tasks : BackgroundTasks):
    user = await get_user_by_email(email, session)

    if user is None:
        raise BadRequestError("No user found for the e-mail")

    otp = await create_otp(session, user.id, usage)

    send_otp_mail(user.email, constants.EmailVerificationOtp, otp, tasks)
    return  UserResponseModel.model_validate(user)