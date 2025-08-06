from datetime import datetime, timezone
import uuid
from sqlalchemy import ForeignKey, Index, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.auth.models.user_model import UserAuth
from src.core.db import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    __table_args__ = (
        Index('idx_password_reset_cleanup', 'exp', 'used'),
        Index('idx_password_reset_user_created', 'user_id', 'created_at'),
    )

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(UserAuth.id, ondelete="CASCADE"), index=True, nullable=False)
    token : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), index=True)
    exp : Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    used : Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)

    user : Mapped["UserAuth"] = relationship(back_populates="pwd_reset_tokens")