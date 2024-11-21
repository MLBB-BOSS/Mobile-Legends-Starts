# File: keyboards/main_keyboard.py
from .base_keyboard import BaseKeyboard

class MainKeyboard(BaseKeyboard):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "🧭 Навігація",
            "🪪 Профіль"
        ]
        return self.create_markup(buttons, row_width=2)
