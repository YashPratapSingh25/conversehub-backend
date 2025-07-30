from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.schemas.register_schema import RegisterSchema
from src.auth.schemas.user_response_schema import UserResponseSchema
from src.core.emails.mail_utils import send_otp_mail
from src.core.exceptions_utils.exceptions import ResourceConflictError
from src.core.hash_utils import generate_hash
from src.auth.utils.get_user_by_email import get_user_by_email
from src.auth.utils.get_user_by_username import get_user_by_username


async def register(session : AsyncSession, schema : RegisterSchema, tasks : BackgroundTasks):

    email_check = await get_user_by_email(schema.email, session)

    if email_check is not None:
        raise ResourceConflictError("User already exists")
    
    username_check = await get_user_by_username(schema.username, session)

    if username_check is not None:
        raise ResourceConflictError("Username already exists")

    new_user = UserAuth(**schema.model_dump())
    new_user.password = generate_hash(schema.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    send_otp_mail(new_user.email, "Mail Testing", "696969", tasks)

    return UserResponseSchema.model_validate(new_user)