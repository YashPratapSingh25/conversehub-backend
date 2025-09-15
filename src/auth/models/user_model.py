from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, DateTime, String, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.core.db import Base

class UserAuth(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password : Mapped[str | None] = mapped_column(String, nullable=True)
    mode : Mapped[str] = mapped_column(String, nullable=False, default="email", server_default="email")
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name : Mapped[str | None] = mapped_column(String, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    refresh_tokens : Mapped[list["RefreshToken"]] = relationship(back_populates="user", passive_deletes=True, cascade="all, delete-orphan") # type: ignore
    sessions : Mapped[list["Session"]] = relationship(back_populates="user", passive_deletes=True, cascade="all, delete-orphan") # type: ignore