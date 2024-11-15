from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from services.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    nickname = Column(String(32), nullable=False)
    email = Column(String, unique=True, nullable=False)
    game_id = Column(String, unique=True, nullable=False)
    is_registered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, nickname={self.nickname}, telegram_id={self.telegram_id})>"
