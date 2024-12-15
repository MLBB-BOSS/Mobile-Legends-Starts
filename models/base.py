from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    """Базовий клас для всіх моделей"""
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
