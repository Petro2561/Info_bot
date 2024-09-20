from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from datetime import datetime, timezone
from typing import Annotated, TypeAlias, Self, Optional
from sqlalchemy import BigInteger, DateTime, Integer, func
from aiogram.enums import ChatType
from aiogram.types import Chat, User


Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now(),
    )

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={Int16: Integer, Int64: BigInteger, datetime: DateTime(timezone=True)}
    )

class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        unique=True, nullable=False, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        unique=False, nullable=True
    )
    first_name: Mapped[str] = mapped_column(
        unique=False, nullable=True
    )
    second_name: Mapped[str] = mapped_column(
        unique=False, nullable=True
    )
    is_admin: Mapped[bool] = mapped_column(default=False)

    @classmethod
    def from_aiogram(cls, user: User) -> Self:
        return cls(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name, 
            second_name=user.last_name,
        )

    def __str__(self):
        return f"{self.first_name}"

