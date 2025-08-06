from datetime import datetime, timezone
import uuid
from sqlalchemy import ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.auth.models.user_model import UserAuth
from src.core.db import Base

class Session(Base):

    __tablename__ = "sessions"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(UserAuth.id, ondelete="CASCADE"), index=True, nullable=False)
    session_name : Mapped[str] = mapped_column(String, nullable=False)
    mode : Mapped[str] = mapped_column(String, nullable=False)
    details : Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    summary_feedack : Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False, index=True)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    saved : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    user : Mapped["UserAuth"] = relationship(back_populates="sessions")
    turns : Mapped[list["Turn"]] = relationship(back_populates="session", passive_deletes=True, cascade="all, delete-orphan") # type: ignore