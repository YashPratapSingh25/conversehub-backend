from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.password_reset_token_model import PasswordResetToken
from src.auth.models.user_model import UserAuth
from src.auth.schemas.forgot_password_schema import ForgotPasswordSchema
from src.auth.schemas.user_response_schema import UserResponseModel
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.auth.services.otp_service import verify_and_revoke_otp
from src.auth.services.get_user_by_email_service import get_user_by_email
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.hash_utils import generate_hash, verify_hash

async def create_and_store_pwd_reset_token_from_otp(schema : VerifyOtpSchema, session : AsyncSession) -> dict:
    otp = await verify_and_revoke_otp(session, schema, "forgot_password")

    pwd_reset_token = uuid4()
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)

    token_obj = PasswordResetToken(
        user_id = otp.user_id,
        token = generate_hash(str(pwd_reset_token)),
        exp = exp
    )

    session.add(token_obj)
    await session.commit()
    await session.refresh(token_obj)

    return {
        "user_id": otp.user_id,
        "password_reset_token": str(pwd_reset_token)
    }

async def verify_and_revoke_pwd_reset_token_and_change_password(schema : ForgotPasswordSchema, session : AsyncSession):
    user = await get_user_by_email(schema.email, session)
    result = await session.execute(
        select(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id)
        .order_by(PasswordResetToken.created_at.desc())
        .limit(1)
    ) 
    reset_token_obj = result.scalar_one_or_none()
    print(reset_token_obj)

    if verify_hash(schema.new_password, user.password):
        raise BadRequestError("New password can't be same as old password.")

    if reset_token_obj is None or not verify_hash(schema.reset_token, reset_token_obj.token) or reset_token_obj.used:
        raise BadRequestError("Invalid token")

    if reset_token_obj.exp < datetime.now(timezone.utc):
        raise BadRequestError("Expired token")
    
    new_password = schema.new_password
    user.password = generate_hash(new_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"user_id": user.id}