from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.core.exceptions_utils.exceptions import BadRequestError

async def get_user_by_id(id : UUID, session : AsyncSession) -> UserAuth | None:
    result = await session.execute(
        select(UserAuth)
        .where(UserAuth.id == id)
    )

    user = result.scalar_one_or_none()

    if user == None:
        raise BadRequestError("Invalid Email")
    
    return user