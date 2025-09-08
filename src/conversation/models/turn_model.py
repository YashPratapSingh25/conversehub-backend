from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.auth.models.user_model import UserAuth
from src.conversation.models.session_model import Session
from src.core.db import Base

class Turn(Base):

    __tablename__ = "turns"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(Session.id, ondelete="CASCADE"), index=True, nullable=False)
    user_text : Mapped[str] = mapped_column(String, nullable=False)
    ai_text : Mapped[str] = mapped_column(String, nullable=False)
    feedback : Mapped[dict] = mapped_column(JSONB, default={}, nullable=False)
    user_speech_link : Mapped[str] = mapped_column(String, nullable=False)
    ai_speech_link : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc), index=True, nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    status : Mapped[str] = mapped_column(String, default="not_completed", index=True, nullable=False)

    session : Mapped["Session"] = relationship(back_populates="turns")