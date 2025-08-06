from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
import uuid
from src.core.db import Base
from src.auth.models.user_model import UserAuth

class Otp(Base):
    __tablename__ = "otp"

    __table_args__ = (
        Index("ix_user_usage_created", "user_id", "usage", "created_at"),
        Index("ix_used_exp", "used", "exp")
    )   

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(UserAuth.id, ondelete="CASCADE"), nullable=False, index=True)
    otp : Mapped[str] = mapped_column(String, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    exp : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    used : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    usage : Mapped[str] = mapped_column(String, nullable=False, index=True)

    user : Mapped["UserAuth"] = relationship(back_populates="otps") # type: ignore