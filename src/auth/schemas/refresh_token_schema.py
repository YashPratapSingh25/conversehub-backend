from uuid import UUID
from src.core.common_schemas import BaseSchema

class RefreshTokenSchema(BaseSchema):
    user_id : str
    refresh_token : str