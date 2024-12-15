from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    level = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_awarded = Column(DateTime, default=datetime.utcnow)

    # Відношення до моделі User
    user = relationship('User', back_populates='badges')

    def __repr__(self):
        return f"<Badge(id={self.id}, name={self.name}, category={self.category})>"
