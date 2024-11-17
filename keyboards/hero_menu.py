# File: keyboards/hero_menu.py
from aiogram.types import InlineKeyboardMarkup
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
        # Використання create_row для створення рядків кнопок
        buttons = [
            cls.create_row(
                {"text": "Tank", "callback_data": "class_tank"},
                {"text": "Fighter", "callback_data": "class_fighter"}
            ),
            cls.create_row(
                {"text": "Assassin", "callback_data": "class_assassin"},
                {"text": "Mage", "callback_data": "class_mage"}
            ),
            cls.create_row(
                {"text": "Marksman", "callback_data": "class_marksman"},
                {"text": "Support", "callback_data": "class_support"}
            )
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
