# keyboards/base_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class BaseKeyboard:
    def create_keyboard(self, buttons: list[list[str]]) -> ReplyKeyboardMarkup:
        keyboard = []
        for row in buttons:
            keyboard_row = [KeyboardButton(text=str(button)) for button in row]
            keyboard.append(keyboard_row)
            
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
