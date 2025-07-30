from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth

async def get_user_by_username(username : str, session : AsyncSession) -> UserAuth | None:
    result = await session.execute(
        select(UserAuth)
        .where(UserAuth.username == username)
    )

    user = result.scalar_one_or_none()

    return user