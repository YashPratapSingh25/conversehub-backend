from uuid import UUID
from src.core.common_schemas import BaseSchema

class RefreshTokenSchema(BaseSchema):
    refresh_token : str