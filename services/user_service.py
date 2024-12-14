from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, default=0)
    achievements_count = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    last_update = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="stats")
    
    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, rating={self.rating}, achievements_count={self.achievements_count})>"
