# models/user.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)  # Changed from user_id to telegram_id
    username = Column(String(50), nullable=True)
    fullname = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    stats = relationship("UserStats", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"