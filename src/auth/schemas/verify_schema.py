from pydantic import BaseModel, EmailStr

class VerifySchema(BaseModel):
    email : EmailStr
    otp : str