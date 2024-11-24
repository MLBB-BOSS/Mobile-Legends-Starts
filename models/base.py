# UTC:22:42
# 2024-11-24
# models/base.py
# Author: MLBB-BOSS
# Description: Base model configuration
# The era of artificial intelligence.

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    pass
