from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    player_id = Column(String, nullable=True)
    game_id = Column(String, nullable=True)  # Поле для збереження ігрового ID
    is_verified = Column(Boolean, default=False)
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)
    tournaments_participated = Column(Integer, default=0)
    tournaments_top3 = Column(Integer, default=0)
    active_months = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Відношення до таблиці badges
    badges = relationship('Badge', secondary='user_badges', back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username}, game_id={self.game_id})>"