from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.core.exceptions_utils.exceptions import BadRequestError

async def get_user_by_email(email : str, session : AsyncSession, registering : bool = False) -> UserAuth | None:
    result = await session.execute(
        select(UserAuth)
        .where(UserAuth.email == email)
    )

    user = result.scalar_one_or_none()

    if user == None:
        if registering:
            return None
        else:
            raise BadRequestError("No user found")
    
    return user