from fastapi import APIRouter
from src.auth.routes.register_api import register_router
from src.auth.routes.resend_otp_api import resend_otp_router
from src.auth.routes.email_otp_verification_api import verify_otp_router
from src.auth.routes.check_username_api import check_username_router
from src.auth.routes.login_api import login_router
from src.auth.routes.refresh_api import refresh_router
from src.auth.routes.logout_api import logout_router
from src.auth.routes.forgot_password_api import forgot_password_router
from src.auth.routes.verify_password_api import verify_password_router
from src.auth.routes.reset_password_api import reset_password_router

auth_router = APIRouter(prefix="/api/auth")

auth_router.include_router(register_router)
auth_router.include_router(resend_otp_router)
auth_router.include_router(verify_otp_router)
auth_router.include_router(check_username_router)
auth_router.include_router(login_router)
auth_router.include_router(refresh_router)
auth_router.include_router(logout_router)
auth_router.include_router(forgot_password_router)
auth_router.include_router(verify_password_router)
auth_router.include_router(reset_password_router)