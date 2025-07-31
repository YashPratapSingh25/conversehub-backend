from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.core.db import Base
from src.auth.models.user_model import UserAuth

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(UserAuth.id, ondelete="CASCADE"), index=True, nullable=False)
    token : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    exp : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    used : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    user_agent : Mapped[str] = mapped_column(String, default=None)
    ip_address : Mapped[str] = mapped_column(String, default=None)

    user : Mapped["UserAuth"] = relationship(back_populates="refresh_tokens")