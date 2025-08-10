from fastapi import APIRouter, Depends, Request
from src.auth.models.user_model import UserAuth
from src.auth.schemas.reset_password_schema import ResetPasswordSchema
from src.auth.services.auth_dependencies import get_current_user
from src.core.limiter import limiter
from src.core.common_schemas import ResponseModel
from src.core.hash_utils import verify_hash

verify_password_router = APIRouter()

@verify_password_router.post('/verify-password', response_model=ResponseModel)
@limiter.limit("3/1minute")
async def verify_password(
    request : Request,
    schema : ResetPasswordSchema,
    user : UserAuth = Depends(get_current_user)
):
    result = verify_hash(schema.password, user.password)
    response = ResponseModel.create_response(data=result, request=request)
    return response