# File: keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    @staticmethod
    def get_main_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Навігація"), KeyboardButton(text="Профіль")]
            ],
            resize_keyboard=True
        )from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    @staticmethod
    def get_main_menu():
        """Генерація головної клавіатури"""
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Навігація"), KeyboardButton(text="Профіль")]
            ],
            resize_keyboard=True
        )
