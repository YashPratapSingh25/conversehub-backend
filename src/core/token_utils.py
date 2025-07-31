from datetime import datetime, timedelta, timezone
from src.core.config import settings
from jose import jwt, JWTError, ExpiredSignatureError

from src.core.exceptions_utils.exceptions import UnauthenticatedError

def encode_token(payload : dict, exp_after : timedelta | None = None) -> str:
    to_encode = payload.copy()

    exp = datetime.now(timezone.utc)
    if exp_after is None:
        exp += timedelta(minutes=settings.ACCESS_TOKEN_DURATION)
    else:
        exp += exp_after

    to_encode.update(
        {"exp": exp}
    )

    access_token = jwt.encode(
        to_encode,
        settings.ACCESS_TOKEN_SECRET_KEY,
        settings.ACCESS_TOKEN_ALGORITHM
    )

    return access_token

def decode_token(token : str) -> dict:
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, settings.ACCESS_TOKEN_ALGORITHM)
    except ExpiredSignatureError:
        raise UnauthenticatedError("Expired Token")
    except JWTError:
        raise UnauthenticatedError("Invalid Token")
    return payload
