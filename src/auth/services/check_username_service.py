from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth

async def check_username_exists(username : str, session : AsyncSession):
    result = await session.execute(
        select(exists().where(UserAuth.username == username))
    )

    check = result.scalar()

    return check