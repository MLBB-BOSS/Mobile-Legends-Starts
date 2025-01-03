# utils/models/item.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from utils.models.base import Base  # Імпорт базового класу

class Item(Base):
    """
    Модель предмету.
    """
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # Встановлення зв'язку з моделлю User
    owner: Mapped["User"] = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
