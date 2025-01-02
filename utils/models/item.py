# utils/models/item.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.base import Base  # Імпорт базового класу

class Item(Base):
    """
    Модель предмету.
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Встановлення зв'язку з моделлю User
    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
