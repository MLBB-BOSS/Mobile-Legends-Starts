# utils/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'  # Використовуйте 'users' для відповідності зовнішнім ключам

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    stats = relationship("UserStats", back_populates="user")
    bug_reports = relationship("BugReport", back_populates="user")