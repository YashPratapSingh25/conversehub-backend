from fastapi import APIRouter
from src.conversation.routers.add_turn_api import add_turn_router
from src.conversation.routers.add_session_api import add_session_router

conversation_router = APIRouter(prefix="/api/conversation")

conversation_router.include_router(add_turn_router)
conversation_router.include_router(add_session_router)