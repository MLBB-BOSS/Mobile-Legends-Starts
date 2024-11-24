# UTC:22:42
# 2024-11-24
# models/user.py
# Author: MLBB-BOSS
# Description: User model
# The era of artificial intelligence.

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    # Primary Key
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    # Telegram Data
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    
    # Game Data
    ml_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    ml_server: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    ml_nickname: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    
    # Heroes Data
    favorite_heroes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    main_role: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    
    # Statistics
    matches_played: Mapped[int] = mapped_column(BigInteger, default=0)
    wins: Mapped[int] = mapped_column(BigInteger, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self) -> str:
        return f"User(id={self.user_id}, username={self.username})"

    @property
    def win_rate(self) -> float:
        """Calculate user's win rate"""
        if self.matches_played == 0:
            return 0.0
        return (self.wins / self.matches_played) * 100
