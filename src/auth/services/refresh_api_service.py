from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.token_utils import encode_token
from src.auth.services.refresh_token_service import create_and_store_refresh_token, verify_and_revoke_refresh_token

async def refresh_api_service(request : Request, refresh_token : str, session : AsyncSession):
    old_token = await verify_and_revoke_refresh_token(complete_token=refresh_token, session=session)
    user_id = old_token.user_id

    new_refresh_token = await create_and_store_refresh_token(request, user_id, session)

    payload = {"sub": str(user_id)}
    new_access_token = encode_token(payload)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "type": "Bearer"
    }