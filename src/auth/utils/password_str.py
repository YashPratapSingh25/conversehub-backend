import re
from typing import Annotated
from pydantic import AfterValidator

def validate_password(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Password must be a string")
    
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if len(value) > 128:
        raise ValueError("Password must not exceed 128 characters")
    
    if not re.search(r'[a-z]', value):
        raise ValueError("Password must contain at least one lowercase letter")
    
    if not re.search(r'[A-Z]', value):
        raise ValueError("Password must contain at least one uppercase letter")
    
    if not re.search(r'\d', value):
        raise ValueError("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("Password must contain at least one special character")
    
    return value

PasswordStr = Annotated[str, AfterValidator(validate_password)]