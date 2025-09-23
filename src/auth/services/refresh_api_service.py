from uuid import UUID
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.refresh_token_schema import RefreshTokenSchema
from src.auth.services.get_user_by_id_service import get_user_by_id
from src.core.token_utils import encode_token
from src.auth.services.refresh_token_service import create_and_store_refresh_token, verify_and_revoke_refresh_token

async def refresh_api_service(schema : RefreshTokenSchema, session : AsyncSession, user_agent, ip_address):
    user_id = schema.user_id
    refresh_token = schema.refresh_token

    user = await get_user_by_id(user_id, session)

    await verify_and_revoke_refresh_token(complete_token=refresh_token, session=session, user=user)

    new_refresh_token = await create_and_store_refresh_token(user_id, session, user_agent, ip_address)

    payload = {"sub": str(user_id)}
    new_access_token = encode_token(payload)

    return {
        "user_id": user_id,
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "type": "Bearer"
    }