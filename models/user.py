# models/user.py

from sqlalchemy import Column, Integer, String
from utils.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    fullname = Column(String, nullable=True)
    level = Column(Integer, default=1)

    stats = relationship("UserStats", back_populates="user", uselist=False)