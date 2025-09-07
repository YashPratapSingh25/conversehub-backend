from bcrypt import checkpw, gensalt, hashpw
import asyncio
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

async def generate_hash(secret : str):
    hash = await asyncio.to_thread(pwd_context.hash, secret)
    return hash

async def verify_hash(secret : str, hash : str):
    check = await asyncio.to_thread(pwd_context.verify, secret, hash)
    return check