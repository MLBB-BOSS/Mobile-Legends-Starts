# models/screenshot.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    file_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="screenshots")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    screenshots = relationship("Screenshot", back_populates="user")
