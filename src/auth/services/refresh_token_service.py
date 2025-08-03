from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.auth.models.refresh_token_model import RefreshToken
from src.core.exceptions_utils.exceptions import BadRequestError, UnauthenticatedError
from src.core.hash_utils import generate_hash, verify_hash
from src.core.config import settings

async def create_and_store_refresh_token(request : Request, user_id : UUID, session : AsyncSession) -> str:
    token_id : UUID = uuid4()
    token : UUID = uuid4()
    complete_token = str(token_id) + "." + str(token)

    refresh_token = RefreshToken(
        id = token_id,
        user_id = user_id,
        token = generate_hash(str(token)),
        exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_DURATION),
        user_agent = request.headers.get('User-Agent', None),
        ip_address = request.client.host
    )

    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)

    return complete_token

async def verify_and_revoke_refresh_token(complete_token : str, session : AsyncSession) -> RefreshToken:
    if len(complete_token.split(".")) != 2:
        raise BadRequestError("Invalid Refresh Token")
    
    token_id = complete_token.split(".")[0]
    token = complete_token.split(".")[1]

    result = await session.execute(
        select(RefreshToken)
        .where(RefreshToken.id == token_id)
    )

    token_obj = result.scalar_one_or_none()

    if not token_obj or not verify_hash(token, token_obj.token) or token_obj.used:
        raise UnauthenticatedError("Invalid Refresh Token")

    if token_obj.exp < datetime.now(timezone.utc):
        raise UnauthenticatedError("Expired Refresh Token")

    token_obj.used = True
    session.add(token_obj)
    await session.commit()
    await session.refresh(token_obj)

    return token_obj