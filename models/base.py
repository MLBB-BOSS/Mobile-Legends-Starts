# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
