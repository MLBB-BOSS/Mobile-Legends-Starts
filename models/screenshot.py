from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

class Screenshot(Base):
    """Модель для зберігання скріншотів"""
    __tablename__ = "screenshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    file_id: Mapped[str] = mapped_column(unique=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Зв'язок з користувачем
    user: Mapped["User"] = relationship(back_populates="screenshots")

    def __repr__(self) -> str:
        return f"Screenshot(id={self.id}, user_id={self.user_id}, file_id={self.file_id})"

class User(Base):
    """Модель користувача"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str | None]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    
    # Зв'язок зі скріншотами
    screenshots: Mapped[List["Screenshot"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})"
