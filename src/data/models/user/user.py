from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, Enum, String, func, text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from src.common.db import Base
from src.domain.user.dto.enums import UserRole


class User(Base):
    id: UUID = Column(
        PostgresUUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    username: str = Column(String(100), nullable=False, unique=True)
    email: str = Column(String(100), nullable=False, unique=True)
    full_name: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)
    role: UserRole = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    is_active: bool = Column(Boolean, nullable=False, server_default="t")
    created_at: datetime = Column(DateTime, nullable=False, server_default=func.now())
    updated_at: datetime = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
