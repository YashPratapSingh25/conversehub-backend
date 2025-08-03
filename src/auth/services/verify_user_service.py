from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.auth.services.otp_service import verify_and_revoke_otp
from src.auth.services.get_user_by_email_service import get_user_by_email
from src.core.exceptions_utils.exceptions import BadRequestError
from src.auth.schemas.user_response_schema import UserResponseModel

async def verify_user(
    session : AsyncSession, 
    schema : VerifyOtpSchema
):
    user = await verify_and_revoke_otp(session, schema, usage="email_verification")

    user.verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserResponseModel.model_validate(user)