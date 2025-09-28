from uuid import UUID
from src.core.common_schemas import BaseSchema

class AuthResponseSchema(BaseSchema):
    user_id : UUID
    access_token : str
    refresh_token : str
    type : str