# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
