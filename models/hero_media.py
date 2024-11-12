# models/hero_media.py
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    SCREENSHOT = "screenshot"

class HeroMedia(BaseModel):
    __tablename__ = 'hero_media'

    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    url = Column(String(512), nullable=False)
    description = Column(String(256))
    
    # Відносини
    hero = relationship("Hero", back_populates="media")

    def __repr__(self):
        return f"<HeroMedia(hero_id={self.hero_id}, type={self.media_type})>"
