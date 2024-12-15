from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    fullname = Column(String(100), nullable=True)

    stats = relationship("UserStats", back_populates="user")