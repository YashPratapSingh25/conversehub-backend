from src.auth.utils.password_str import PasswordStr
from src.core.common_schemas import BaseSchema

class ResetPasswordSchema(BaseSchema):
    password : PasswordStr