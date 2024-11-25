# UTC:22:42
# 2024-11-24
# models/user.py
# Author: MLBB-BOSS
# Description: User model
# The era of artificial intelligence.

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from models.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Унікальний ID
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram ID
    username = Column(String(50), nullable=True)  # Ім'я користувача
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата створення

    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id}, username={self.username})>"
