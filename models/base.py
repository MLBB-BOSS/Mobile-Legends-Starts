# models/base.py

from .user import User
from .badge import Badge
from .user_badges import user_badges
from .user_stats import UserStats
# Додайте інші моделі за потребою
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
