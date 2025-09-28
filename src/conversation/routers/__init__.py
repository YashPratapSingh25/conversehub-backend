from fastapi import APIRouter
from src.conversation.routers.add_turn_api import add_turn_router
from src.conversation.routers.add_session_api import add_session_router
from src.conversation.routers.get_sas_token_api import sas_token_router
from src.conversation.routers.get_sessions_api import get_sessions_router

conversation_router = APIRouter(prefix="/api/conversation")

conversation_router.include_router(add_turn_router)
conversation_router.include_router(add_session_router)
conversation_router.include_router(sas_token_router)
conversation_router.include_router(get_sessions_router)