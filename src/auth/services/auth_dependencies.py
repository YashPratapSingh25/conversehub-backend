from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token : str):
    pass