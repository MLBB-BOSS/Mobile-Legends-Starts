# utils/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from utils.base import Base  # Імпорт базового класу
from typing import List

class User(Base):
    """
    Модель користувача.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # Додайте інші поля за потребою

    # Встановлення зв'язку з моделлю Item
    items: List["Item"] = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
