from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from src.auth.models.user_model import UserAuth
from src.conversation.models.session_model import Session
from src.conversation.schemas.delete_session_schema import DeleteSessionSchema

async def delete_session_service(
    db_session : AsyncSession,
    schema : DeleteSessionSchema
):
    await db_session.execute(
        delete(Session)
        .where(Session.id == schema.session_id)
    )

    await db_session.commit()