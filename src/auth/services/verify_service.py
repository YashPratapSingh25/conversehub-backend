from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.verify_schema import VerifySchema
from src.auth.services.otp_service import verify_otp
from src.auth.utils.get_user_by_email import get_user_by_email
from src.core.exceptions_utils.exceptions import BadRequestError
from src.auth.schemas.user_response_schema import UserResponseModel
from src.core.constants import constants

async def verify_user_service(
    session : AsyncSession, 
    schema : VerifySchema
):
    user = await get_user_by_email(schema.email, session)

    if user is None:
        raise BadRequestError("No user found for the e-mail")

    await verify_otp(session, user.id, schema.otp, usage=constants.EmailVerificationUsage)

    user.verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return UserResponseModel.model_validate(user)