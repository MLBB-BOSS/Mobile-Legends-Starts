# models/contribution.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base

class Contribution(Base):
    __tablename__ = 'contributions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    contribution_type = Column(String, index=True)
    points = Column(Integer)
    date = Column(String)

    # Ставимо відношення до таблиці "User" (потрібно створити модель користувачів)
    user = relationship("User", back_populates="contributions")

    def __repr__(self):
        return f"<Contribution(user_id={self.user_id}, contribution_type={self.contribution_type}, points={self.points})>"
