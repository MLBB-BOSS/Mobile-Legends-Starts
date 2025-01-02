# utils/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from utils.base import Base  # Імпорт базового класу

class User(Base):
    """
    Модель користувача.
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Додайте інші поля за потребою

    # Встановлення зв'язку з моделлю Item
    items: Mapped[List["Item"]] = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
