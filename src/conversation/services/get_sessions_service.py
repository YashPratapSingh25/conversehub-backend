from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.conversation.models.session_model import Session
from src.conversation.schemas.session_response_schema import SessionResponseSchema
from src.core.logger import logger

async def get_sessions(
    limit : int,
    offset : int,
    db_session : AsyncSession,
    user : UserAuth
):
    result = await db_session.execute(
        select(Session)
        .where(Session.user_id == user.id)
        .order_by(Session.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )

    sessions = list(result.scalars().all())

    return [SessionResponseSchema.model_validate(session) for session in sessions]