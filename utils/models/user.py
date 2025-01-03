# utils/models/users.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Відношення
    stats = relationship("UserStats", back_populates="user", uselist=False)
    feedbacks = relationship("Feedback", back_populates="user")
    bug_reports = relationship("BugReport", back_populates="user")

class UserStats(Base):
    __tablename__ = 'user_stats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tournaments_played = Column(Integer, default=0)
    tournaments_won = Column(Integer, default=0)
    matches_played = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    total_screenshots = Column(Integer, default=0)
    achievements_count = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Відношення
    user = relationship("User", back_populates="stats")
