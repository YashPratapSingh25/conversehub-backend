from uuid import UUID
from src.core.common_schemas import BaseSchema

class AuthResponseSchema(BaseSchema):
    user_id : UUID
    first_name : str
    last_name : str
    access_token : str
    refresh_token : str
    type : str