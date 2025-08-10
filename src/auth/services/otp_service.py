from datetime import datetime, timedelta, timezone
from uuid import UUID
from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint
from src.auth.models.user_model import UserAuth
from src.auth.schemas.user_response_schema import UserResponseModel
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.auth.services.get_user_by_email_service import get_user_by_email
from src.core.emails.mail_utils import send_otp_mail
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.hash_utils import generate_hash, verify_hash
from src.auth.models.otp_model import Otp

async def create_and_store_otp(session : AsyncSession, user_id : UUID, usage : str) -> str:
    otp = str(randint(100000, 999999))
    exp = datetime.now(timezone.utc) + timedelta(minutes=5)
    hashed_otp = generate_hash(otp)

    otp_obj = Otp(user_id=user_id, otp=hashed_otp, exp=exp, usage = usage)

    session.add(otp_obj)
    await session.commit()
    await session.refresh(otp_obj)

    return otp

async def verify_and_revoke_otp(session : AsyncSession, schema : VerifyOtpSchema, usage : str) -> Otp:
    user = await get_user_by_email(schema.email, session)
    result = await session.execute(
        select(Otp)
        .where(
            Otp.user_id == user.id, 
            Otp.usage == usage
        )
        .order_by(Otp.created_at.desc())
        .limit(1)
    )

    otp_obj = result.scalar_one_or_none()

    if otp_obj is None:
        raise BadRequestError("No OTP found for the e-mail")
    
    if otp_obj.exp < datetime.now(timezone.utc):
        raise BadRequestError("Expired OTP")
    
    if not verify_hash(schema.otp, otp_obj.otp) or otp_obj.used:
        raise BadRequestError("Invalid OTP")
    
    otp_obj.used = True
    session.add(otp_obj)
    await session.commit()
    await session.refresh(otp_obj)
    return otp_obj

async def send_otp(email : str, session : AsyncSession, usage : str, tasks : BackgroundTasks, user : UserAuth | None = None):
    if user is None:
        user = await get_user_by_email(email, session)

    otp = await create_and_store_otp(session, user.id, usage)

    if usage == "email_verification":
        subject = "Email Verification"
    elif usage == "forgot_password":
        subject = "Forgot Password"

    send_otp_mail(email, subject, otp, tasks)
    return  {"user_id": user.id}