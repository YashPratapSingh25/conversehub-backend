from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.schemas.register_schema import RegisterSchema
from src.auth.schemas.user_response_schema import UserResponseModel
from src.auth.services.check_username_service import check_username_exists
from src.auth.services.otp_service import create_otp
from src.core.constants import constants
from src.core.emails.mail_utils import send_otp_mail
from src.core.exceptions_utils.exceptions import ResourceConflictError
from src.core.hash_utils import generate_hash
from src.auth.services.get_user_by_email_service import get_user_by_email


async def register(
    session : AsyncSession, 
    schema : RegisterSchema, 
    tasks : BackgroundTasks) -> UserResponseModel:

    email_check = await get_user_by_email(schema.email, session)

    if email_check is not None:
        raise ResourceConflictError("User already exists")
    
    username_exists = await check_username_exists(schema.username, session)

    if username_exists:
        raise ResourceConflictError("Username already exists")

    new_user = UserAuth(**schema.model_dump())
    new_user.password = generate_hash(schema.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    otp = await create_otp(session, new_user.id, constants.EmailVerificationUsage)

    send_otp_mail(new_user.email, constants.EmailVerificationOtp, otp, tasks)

    return UserResponseModel.model_validate(new_user)