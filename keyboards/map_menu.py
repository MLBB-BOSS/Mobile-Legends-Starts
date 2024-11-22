# keyboards/map_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MapMenu:
    """Клавіатура для розділу 'Інтерактивна Карта' (3-й рівень)"""
    @staticmethod
    def get_map_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🏞️ Огляд Мап"), KeyboardButton(text="📍 Тактики на Картах")],
                [KeyboardButton(text="🕹️ Практика на Мапі"), KeyboardButton(text="🔄 Назад до Навігації")],
            ],
            resize_keyboard=True
        )
