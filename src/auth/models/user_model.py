from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.core.db import Base

class UserAuth(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password : Mapped[str] = mapped_column(String, nullable=False)
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name : Mapped[str | None] = mapped_column(String, nullable=True)
    verified : Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False, index=True)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    otps: Mapped[list["Otp"]] = relationship(back_populates="user", passive_deletes=True, cascade="all, delete-orphan") # type: ignore