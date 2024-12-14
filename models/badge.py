# models/badge.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Зворотне відношення до користувачів через асоціативну таблицю
    users = relationship('User', secondary='user_badges', back_populates='badges')
