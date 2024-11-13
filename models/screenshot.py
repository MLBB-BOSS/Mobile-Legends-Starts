from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .base import Base

class Screenshot(Base):
    __tablename__ = 'screenshots'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)  # Telegram user ID
    file_id = Column(String, nullable=False)   # Telegram file ID
    hero_name = Column(String, nullable=True)  # Name of the hero in screenshot
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Screenshot(id={self.id}, user_id={self.user_id}, hero_name={self.hero_name})>"
