from uuid import UUID

from pydantic import EmailStr
from src.core.common_schemas import BaseSchema

class ForgotPasswordSchema(BaseSchema):
    email : EmailStr
    reset_token : str
    new_password : str