from typing import Optional
from pydantic import EmailStr, Field
from src.auth.utils.password_str import PasswordStr
from src.auth.utils.username_str import UsernameStr
from src.core.common_schemas import BaseSchema

class RegisterSchema(BaseSchema):
    username : UsernameStr
    email : EmailStr
    password : PasswordStr
    first_name : str
    last_name : Optional[str] = Field(default=None)