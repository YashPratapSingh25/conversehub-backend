from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from src.auth.models.refresh_token_model import RefreshToken
from src.core.hash_utils import generate_hash, verify_hash
from src.core.config import settings

async def create_refresh_token(request : Request, user_id : UUID, session : AsyncSession) -> str:
    token_id : UUID = uuid4()
    token : UUID = uuid4()
    complete_token = str(token_id) + "." + str(token)

    refresh_token = RefreshToken(
        id = token_id,
        user_id = user_id,
        token = generate_hash(complete_token),
        exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_DURATION),
        user_agent = request.headers.get('User-Agent', None),
        ip_address = request.client.host
    )

    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)

    return complete_token