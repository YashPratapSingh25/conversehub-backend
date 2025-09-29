from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from src.auth.schemas.auth_response_schema import AuthResponseSchema
from src.auth.services.get_create_user_service import get_or_create_user
from src.auth.schemas.google_auth_schema import GoogleAuthSchema
from src.auth.services.refresh_token_service import create_and_store_refresh_token
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.config import settings
from src.core.token_utils import encode_token

async def auth_with_google(
    request : Request,
    schema : GoogleAuthSchema,
    session : AsyncSession
):
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={schema.id_token}")
    
    if response.status_code != 200:
        raise BadRequestError("Invalid Google token")
    
    profile = response.json()

    if profile.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise BadRequestError("Token not meant for this app")
    
    user_email = profile.get("email")
    first_name = profile.get("given_name")
    last_name = profile.get("family_name")
    
    user = await get_or_create_user(session=session, email=user_email, first_name=first_name, last_name=last_name)
    access_token = encode_token({"sub": str(user.id)})
    refresh_token = await create_and_store_refresh_token(user.id, session, request.headers.get("User-Agent"), request.client.host)
    
    return AuthResponseSchema(
        user_id = user.id,
        first_name = user.first_name,
        last_name = user.last_name,
        access_token = access_token,
        refresh_token = refresh_token,
        type = "Bearer"
    )