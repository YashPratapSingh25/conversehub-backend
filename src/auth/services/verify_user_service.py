from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.verify_email_schema import VerifyOtpSchema
from src.auth.services.otp_service import verify_and_revoke_otp
from src.auth.services.get_user_by_id_service import get_user_by_id as get_user 
from src.core.exceptions_utils.exceptions import BadRequestError
from src.auth.schemas.user_response_schema import UserResponseModel

async def verify_user(
    session : AsyncSession, 
    schema : VerifyOtpSchema
):
    otp = await verify_and_revoke_otp(session, schema, usage="email_verification")
    user = await get_user(otp.user_id, session)

    user.verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"user_id": user.id}