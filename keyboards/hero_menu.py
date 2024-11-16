from .base import BaseKeyboard
from aiogram.types import InlineKeyboardMarkup

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
    def get_class_keyboard(cls) -> InlineKeyboardMarkup:
        """Повертає клавіатуру з класами героїв"""
        buttons = [
            [
                {"text": "Tank", "callback_data": "class_tank"},
                {"text": "Fighter", "callback_data": "class_fighter"}
            ],
            [
                {"text": "Assassin", "callback_data": "class_assassin"},
                {"text": "Mage", "callback_data": "class_mage"}
            ],
            [
                {"text": "Marksman", "callback_data": "class_marksman"},
                {"text": "Support", "callback_data": "class_support"}
            ]
        ]
        return cls.create_keyboard(buttons, is_inline=True)

    @classmethod
    def get_heroes_keyboard(cls, hero_class: str) -> InlineKeyboardMarkup:
        """Повертає клавіатуру з героями конкретного класу"""
        buttons = []
        for hero in cls._heroes.get(hero_class.lower(), []):
            buttons.append([{
                "text": hero,
                "callback_data": f"hero_{hero.lower()}"
            }])
        
        buttons.append([{
            "text": "⬅️ Назад",
            "callback_data": "back_to_classes"
        }])
        return cls.create_keyboard(buttons, is_inline=True)
