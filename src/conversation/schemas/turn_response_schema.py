from datetime import datetime
from uuid import UUID
from src.core.common_schemas import BaseSchema

class TurnResponseSchema(BaseSchema):
    id : UUID
    transcription : str
    llm_response : dict
    user_speech : str
    ai_speech : str
    created_at : datetime
    updated_at : datetime