# models/hero.py
from sqlalchemy import Column, String, Text, Enum, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class HeroRole(enum.Enum):
    TANK = "Tank"
    FIGHTER = "Fighter"
    ASSASSIN = "Assassin"
    MAGE = "Mage"
    MARKSMAN = "Marksman"
    SUPPORT = "Support"

class Hero(BaseModel):
    __tablename__ = 'heroes'

    name = Column(String(64), unique=True, nullable=False)
    role = Column(Enum(HeroRole), nullable=False)
    description = Column(Text)
    difficulty = Column(Integer)  # 1-3 складність героя
    
    # Відносини
    media = relationship("HeroMedia", back_populates="hero")
    guides = relationship("HeroGuide", back_populates="hero")

    def __repr__(self):
        return f"<Hero(name={self.name}, role={self.role})>"
