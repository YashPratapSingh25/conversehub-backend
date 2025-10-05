from datetime import datetime
from uuid import UUID
from src.core.common_schemas import BaseSchema

class SessionResponseSchema(BaseSchema):
    id : UUID
    user_id : UUID
    session_name : str
    mode : str
    details : dict
    summary_feedback : dict
    created_at : datetime
    updated_at : datetime