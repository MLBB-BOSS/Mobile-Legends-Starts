# models/hero_guide.py
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class HeroGuide(BaseModel):
    __tablename__ = 'hero_guides'

    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, default=0)
    
    # Відносини
    hero = relationship("Hero", back_populates="guides")
    author = relationship("User")

    def __repr__(self):
        return f"<HeroGuide(hero_id={self.hero_id}, title={self.title})>"
