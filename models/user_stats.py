# models/user_stats.py

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

class UserStats(Base):
    __tablename__ = 'user_stats'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, default=0)
    achievements_count = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    last_update = Column(DateTime, default=datetime.utcnow)
    activity_history = Column(String, default="")  # Зберігає історію активності у форматі CSV, наприклад: "70,75,80,85,90,95,100"

    user = relationship("User", back_populates="stats")

    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, rating={self.rating}, achievements={self.achievements_count})>"