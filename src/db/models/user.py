from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class User(Base):
    """
    Entidade de Usuário.
    @property {UUID} id - Identificador único (UUIDv4).
    @property {str} email - E-mail único do usuário (normalizado em minúsculas).
    @property {str} password_hash - Hash da senha do usuário (bcrypt).
    @property {bool} is_active - Flag de ativação.
    @property {datetime} created_at - Carimbo de criação.
    """
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), nullable=False)  # 320 = RFC
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
