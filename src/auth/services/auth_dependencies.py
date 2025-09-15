from uuid import UUID
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from src.auth.models.user_model import UserAuth
from src.core.db import session_maker
from src.core.exceptions_utils.exceptions import UnauthenticatedError
from src.core.token_utils import decode_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/google")

async def get_current_user(request : Request, token : str = Depends(oauth_scheme)):
    payload = decode_token(token)
    str_id = payload.get("sub")

    if str_id is None:
        raise UnauthenticatedError("Invalid Token")

    try:
        user_id = UUID(str_id)
    except:
        raise UnauthenticatedError("Invalid Token")

    async with session_maker() as session:
        
        result = await session.execute(
            select(UserAuth)
            .where(UserAuth.id == user_id)
        )

        user = result.scalar_one_or_none()

        if user is None:
            raise UnauthenticatedError("Invalid Token")

    request.state.user = user.id
        
    return user