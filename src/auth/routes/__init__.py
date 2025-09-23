from fastapi import APIRouter
from src.auth.routes.refresh_api import refresh_router
from src.auth.routes.logout_api import logout_router
from src.auth.routes.google_auth_api import google_auth_router
from src.auth.routes.check_access_token_api import check_access_token_router

auth_router = APIRouter(prefix="/api/auth")

auth_router.include_router(refresh_router)
auth_router.include_router(logout_router)
auth_router.include_router(google_auth_router)
auth_router.include_router(check_access_token_router)