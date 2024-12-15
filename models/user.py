from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
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
    created_at = Column(DateTime, default=datetime.utcnow)

    # Відношення до badges та stats
    badges = relationship("Badge", back_populates="user")
    stats = relationship("UserStats", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"
