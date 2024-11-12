from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import BaseModel

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    GUIDE = "guide"

class HeroMedia(BaseModel):
    __tablename__ = 'hero_media'
    
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(String(1000))
    
    # Система голосування
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    
    # Відносини
    hero = relationship("Hero", back_populates="media")
    
    @property
    def rating(self) -> float:
        """Обчислює рейтинг медіа контенту"""
        total = self.upvotes + self.downvotes
        if total == 0:
            return 0
        return self.upvotes / total * 100
