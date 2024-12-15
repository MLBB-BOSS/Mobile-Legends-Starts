# models/badge.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
