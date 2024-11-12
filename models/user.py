# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(32), unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    is_admin = Column(Boolean, default=False)
    experience = Column(Integer, default=0)
    level = Column(Integer, default=1)
    bio = Column(Text)
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"# Модель користувача
