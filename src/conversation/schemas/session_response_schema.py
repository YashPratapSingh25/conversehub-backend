from datetime import datetime
from uuid import UUID
from src.core.common_schemas import BaseSchema

class CreateSessionResponseSchema(BaseSchema):
    id : UUID
    session_name : str
    mode : str
    created_at : datetime