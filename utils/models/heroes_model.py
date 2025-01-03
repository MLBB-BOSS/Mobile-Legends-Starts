# models/heroes_model.py
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Hero(Base):
    """
    Модель для таблиці героїв.
    """
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    hero_class = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    # Відношення до навичок героя
    skills = relationship("Skill", back_populates="hero")

class Skill(Base):
    """
    Модель для таблиці навичок героїв.
    """
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cooldown = Column(Integer, nullable=True)
    mana_cost = Column(Integer, nullable=True)

    # Зовнішній ключ на героя
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=False)
    hero = relationship("Hero", back_populates="skills")
