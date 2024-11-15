from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class Hero(Base):
    """Модель героя Mobile Legends"""
    
    name: Mapped[str] = mapped_column(unique=True)
    hero_class: Mapped[str]
    role: Mapped[str]
    specialty: Mapped[str]
    difficulty: Mapped[int]
    description: Mapped[Optional[str]]
    image_url: Mapped[Optional[str]]
    
    # Статистика героя
    hp: Mapped[float]
    mana: Mapped[float]
    physical_attack: Mapped[float]
    magic_power: Mapped[float]
    armor: Mapped[float]
    magic_resistance: Mapped[float]
    movement_speed: Mapped[float]
    
    @property
    def stats_dict(self) -> dict:
        """Повертає статистику героя у вигляді словника"""
        return {
            "hp": self.hp,
            "mana": self.mana,
            "physical_attack": self.physical_attack,
            "magic_power": self.magic_power,
            "armor": self.armor,
            "magic_resistance": self.magic_resistance,
            "movement_speed": self.movement_speed
        }
