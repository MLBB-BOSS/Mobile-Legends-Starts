# File: keyboards/hero_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .base import BaseKeyboard

class HeroMenu(BaseKeyboard):
    """Меню вибору героїв"""
    
    _heroes = {
        "tank": ["Tigreal", "Franco", "Minotaur"],
        "fighter": ["Alucard", "Zilong", "Balmond"],
        "assassin": ["Saber", "Fanny", "Karina"],
        "mage": ["Eudora", "Gord", "Aurora"],
        "marksman": ["Layla", "Miya", "Bruno"],
        "support": ["Rafaela", "Estes", "Angela"]
    }

    @classmethod
    def get_class_keyboard(cls):
        """Повертає клавіатуру з класами героїв"""
        buttons = [
            "Tank", "Fighter",
            "Assassin", "Mage",
            "Marksman", "Support"
        ]
        return cls.create_keyboard(
            buttons=buttons,
            row_width=2,
            resize_keyboard=True
        )

    @classmethod
    def get_heroes_keyboard(cls, hero_class: str):
        """Повертає клавіатуру з героями вибраного класу"""
        if hero_class.lower() not in cls._heroes:
            return None
        
        buttons = cls._heroes[hero_class.lower()]
        buttons.append("↩️ Назад до класів")
        
        return cls.create_keyboard(
            buttons=buttons,
            row_width=2,
            resize_keyboard=True
        )
