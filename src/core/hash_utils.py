from bcrypt import checkpw, gensalt, hashpw

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def generate_hash(secret : str):
    hash = pwd_context.hash(secret)
    return hash

def verify_hash(secret : str, hash : str):
    return pwd_context.verify(secret, hash)