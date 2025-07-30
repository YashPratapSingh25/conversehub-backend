from typing import Annotated
from pydantic import AfterValidator
import re

def validate_string(value : str) -> str:
    
    if not isinstance(value, str):
        raise ValueError("Username must be a string")
    
    if len(value) < 3 or len(value) > 20:
        raise ValueError("Username must be between 3 and 20 characters")
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError("Username can only contain letters, numbers, underscores, and hyphens")
    
    if not re.match(r'^[a-zA-Z]', value):
        raise ValueError("Username must start with a letter")
    
    return value

UsernameStr = Annotated[str, AfterValidator(validate_string)]