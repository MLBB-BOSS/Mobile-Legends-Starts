# models/user_stats.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from utils.db import Base

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, default=0.0)
    total_matches = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    activity = Column(Float, default=0.0)
    activity_history = Column(String, nullable=True)
    achievements_count = Column(Integer, default=0)
    last_update = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="stats")