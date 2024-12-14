# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    level = Column(String, default="Новачок")
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)

    # Зв’язок з бейджами
    badges = relationship("Badge", back_populates="user")

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    level = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="badges")
    date_awarded = Column(DateTime, default=datetime.utcnow)
