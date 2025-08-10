from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.auth.schemas.reset_password_schema import ResetPasswordSchema
from src.auth.schemas.user_response_schema import UserResponseModel
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.hash_utils import generate_hash, verify_hash

async def reset_password(session : AsyncSession, schema : ResetPasswordSchema, user : UserAuth):
    if verify_hash(schema.password, user.password):
        raise BadRequestError("New password can't be same as old password.")
    
    user.password = generate_hash(schema.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"user_id": user.id}