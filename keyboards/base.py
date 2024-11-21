# keyboards/base.py - базовий клас для створення клавіатур

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BaseKeyboard:
    @staticmethod
    def create_inline_keyboard(buttons: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        """Створює InlineKeyboardMarkup."""
        for row in buttons:
            if not all(isinstance(button, InlineKeyboardButton) for button in row):
                raise ValueError("Всі елементи мають бути InlineKeyboardButton")
        return InlineKeyboardMarkup(inline_keyboard=buttons)
