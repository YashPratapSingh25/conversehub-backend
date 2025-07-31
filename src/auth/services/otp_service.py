from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from random import randint
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.hash_utils import generate_hash, verify_hash
from src.auth.models.otp_model import Otp

async def create_otp(session : AsyncSession, user_id : UUID, usage : str) -> str:
    otp = str(randint(100000, 999999))
    exp = datetime.now(timezone.utc) + timedelta(minutes=5)
    hashed_otp = generate_hash(otp)

    otp_obj = Otp(user_id=user_id, otp=hashed_otp, exp=exp, usage = usage)

    session.add(otp_obj)
    await session.commit()
    await session.refresh(otp_obj)

    return otp

async def verify_otp(session : AsyncSession, user_id : UUID, otp : str, usage : str):
    result = await session.execute(
        select(Otp)
        .where(Otp.user_id == user_id, Otp.usage == usage)
        .order_by(Otp.created_at.desc())
        .limit(1)
    )

    otp_obj = result.scalar_one_or_none()

    if otp_obj is None:
        raise BadRequestError("No OTP found for the e-mail")
    
    if otp_obj.exp < datetime.now(timezone.utc):
        raise BadRequestError("Expired OTP")
    
    if not verify_hash(otp, otp_obj.otp) or otp_obj.used:
        raise BadRequestError("Invalid OTP")
    
    otp_obj.used = True
    session.add(otp_obj)
    session.commit()
    session.refresh(otp_obj)