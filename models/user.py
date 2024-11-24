# models/user.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Модель користувача для бази даних

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.username or self.telegram_id}>"
