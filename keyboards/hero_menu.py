# File: keyboards/heroes.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class HeroesKeyboard(BaseKeyboard):
    @classmethod
    def get_classes(cls) -> ReplyKeyboardMarkup:
        """Hero classes selection keyboard"""
        hero_classes = [
            "heroes.classes.tank.name",
            "heroes.classes.fighter.name",
            "heroes.classes.assassin.name",
            "heroes.classes.mage.name",
            "heroes.classes.marksman.name",
            "heroes.classes.support.name"
        ]
        return cls.create_keyboard(
            hero_classes, 
            row_width=3,
            back_key="buttons.back_to_navigation"
        )

    @classmethod
    def get_heroes_by_class(cls, hero_class: str) -> ReplyKeyboardMarkup:
        """Heroes list keyboard for specific class"""
        heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")
        return cls.create_keyboard(
            heroes,
            row_width=3,
            back_key="buttons.back_to_hero_classes"
        )
