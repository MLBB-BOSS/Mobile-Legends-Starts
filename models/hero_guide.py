from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class HeroGuide(BaseModel):
    __tablename__ = 'hero_guides'
    
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    # Статистика
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    
    # Відносини
    hero = relationship("Hero", back_populates="guides")
    author = relationship("User", back_populates="guides")
    
    def increment_views(self):
        """Збільшує лічильник переглядів"""
        self.views += 1
