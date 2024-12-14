# models/user_stats.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserStats(Base):
    __tablename__ = 'user_stats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    # Додайте інші поля статистики за потребою

    # Відношення до користувача
    user = relationship('User', back_populates='stats')