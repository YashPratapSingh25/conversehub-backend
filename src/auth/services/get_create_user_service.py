from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.services.check_username_service import check_username_exists
from src.auth.services.get_user_by_email_service import get_user_by_email
from random import randint

async def get_or_create_user(
    session : AsyncSession,
    email : str,
    first_name : str,
    last_name : str
) -> UserAuth:
    user_exists = await get_user_by_email(email=email, session=session)

    if not user_exists:
        username = email.split("@")[0]
        if await check_username_exists(username, session):
            random = str(randint(0000, 9999))
            username += random
        new_user = UserAuth(
            username = username,
            email = email,
            mode = "google",
            first_name = first_name,
            last_name = last_name
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        return new_user
    else:
        return user_exists