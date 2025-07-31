from datetime import datetime
from typing import Optional
from src.core.common_schemas import BaseSchema

class UserResponseModel(BaseSchema):
    username : str
    email : str
    first_name : str
    last_name : Optional[str]
    created_at : datetime
    updated_at : datetime