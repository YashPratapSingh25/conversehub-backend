from pydantic import EmailStr
from src.auth.utils.password_str import PasswordStr
from src.core.common_schemas import BaseSchema


class LoginSchema(BaseSchema):
    email : EmailStr
    password : PasswordStr