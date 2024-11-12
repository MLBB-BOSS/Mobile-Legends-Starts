from typing import List, Optional
from sqlalchemy import Column, String, Integer, Float, Text
from .base import BaseModel

class Hero(BaseModel):
    __tablename__ = 'heroes'
    
    name = Column(String(100), nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    difficulty = Column(Integer, nullable=False)
    
    # Базові характеристики
    hp = Column(Float, nullable=False)
    mana = Column(Float, nullable=False)
    physical_attack = Column(Float, nullable=False)
    magic_power = Column(Float, nullable=False)
    
    # Пошуковий текст для швидкого пошуку
    search_text = Column(Text)
    
    # Метадані
    popularity = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    
    def update_search_text(self):
        """Оновлює пошуковий текст для героя"""
        self.search_text = f"{self.name} {self.role}".lower()
