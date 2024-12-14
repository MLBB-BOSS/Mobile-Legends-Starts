# models/badge.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)  # Припустимо, що тут зберігаються емодзі або URL до іконки

    users = relationship("User", secondary="user_badges", back_populates="badges")

    def __repr__(self):
        return f"<Badge(id={self.id}, name={self.name})>"