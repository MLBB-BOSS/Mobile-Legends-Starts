# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    level = Column(String, default="Новачок")
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)

    # Відношення до UserStats (один до одного)
    stats = relationship("UserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Відношення до Badge (один до багатьох)
    badges = relationship("Badge", back_populates="user", cascade="all, delete-orphan")