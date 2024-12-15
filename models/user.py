# models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    player_id = Column(String, nullable=True)  # ID користувача у системі
    game_id = Column(String, nullable=True)  # Ігровий ID Mobile Legends
    is_verified = Column(Boolean, default=False)  # Чи верифікований користувач
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)
    tournaments_participated = Column(Integer, default=0)
    tournaments_top3 = Column(Integer, default=0)
    active_months = Column(Integer, default=0)
    level = Column(String, default="Beginner")  # Новий стовпець
    badges = relationship("Badge", secondary="user_badges", back_populates="users")
    created_at = Column(DateTime, default=datetime.utcnow)
