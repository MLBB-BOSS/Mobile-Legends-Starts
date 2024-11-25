# UTC:22:42
# 2024-11-24
# models/base.py
# Author: MLBB-BOSS
# Description: Base model configuration
# The era of artificial intelligence.

from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
