from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

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
    badges = relationship("Badge", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow)

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    level = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="badges")
    date_awarded = Column(DateTime, default=datetime.utcnow)