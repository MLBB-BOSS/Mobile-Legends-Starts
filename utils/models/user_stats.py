# models/user_stats.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from utils.db import Base
from datetime import datetime

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    level = Column(Integer, default=1)
    rating = Column(Integer, default=1000)
    achievements_count = Column(Integer, default=0)
    screenshots_count = Column(Integer, default=0)
    missions_count = Column(Integer, default=0)
    quizzes_count = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    tournament_participations = Column(Integer, default=0)
    badges_count = Column(Integer, default=0)
    last_update = Column(DateTime, default=datetime.utcnow)

    # Відношення до користувача
    user = relationship("User", back_populates="stats")
