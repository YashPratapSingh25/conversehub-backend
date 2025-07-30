from fastapi import APIRouter
from src.auth.routes.register_api import register_router

auth_router = APIRouter(prefix="/api/auth")

auth_router.include_router(register_router)