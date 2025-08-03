from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas.login_schema import LoginSchema
from src.auth.services.get_user_by_email_service import get_user_by_email
from src.auth.services.refresh_token_service import create_and_store_refresh_token
from src.core.exceptions_utils.exceptions import UnauthenticatedError
from src.core.hash_utils import verify_hash
from src.core.token_utils import encode_token

async def login_user(
    request : Request,
    schema : LoginSchema,
    session : AsyncSession
) -> dict: 
    user = await get_user_by_email(schema.email, session)

    if not user.verified:
        raise UnauthenticatedError("Email not verified")

    if not verify_hash(schema.password, user.password):
        raise UnauthenticatedError("Invalid Credentials")
    
    access_token = encode_token({
        "sub": str(user.id)
    })

    refresh_token = await create_and_store_refresh_token(request, user.id, session)

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "type": "Bearer"
    }

    return response