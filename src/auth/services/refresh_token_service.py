from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.auth.models.refresh_token_model import RefreshToken
from src.auth.models.user_model import UserAuth
from src.core.exceptions_utils.exceptions import BadRequestError, ForbiddenError, UnauthenticatedError
from src.core.hash_utils import generate_hash, verify_hash
from src.core.config import settings

async def create_and_store_refresh_token(user_id : UUID, session : AsyncSession, user_agent, ip_address) -> str:
    token_id : UUID = uuid4()
    token : UUID = uuid4()
    complete_token = str(token_id) + "." + str(token)

    refresh_token = RefreshToken(
        id = token_id,
        user_id = user_id,
        token = await generate_hash(str(token)),
        exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_DURATION),
        user_agent = user_agent,
        ip_address = ip_address
    )

    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)

    return complete_token

async def verify_and_revoke_refresh_token(complete_token : str, session : AsyncSession, user : UserAuth) -> RefreshToken:
    if len(complete_token.split(".")) != 2:
        raise BadRequestError("Invalid Refresh Token")
    
    token_id = complete_token.split(".")[0]
    token = complete_token.split(".")[1]

    result = await session.execute(
        select(RefreshToken)
        .where(RefreshToken.id == token_id)
    )

    token_obj = result.scalar_one_or_none()

    if token_obj.user_id != user.id:
        raise ForbiddenError("Invalid Refresh Token for the user")

    if not token_obj or not await verify_hash(token, token_obj.token) or token_obj.used:
        raise UnauthenticatedError("Invalid Refresh Token")

    if token_obj.exp < datetime.now(timezone.utc):
        raise UnauthenticatedError("Expired Refresh Token")

    token_obj.used = True
    await session.delete(token_obj)
    await session.commit()

    return token_obj