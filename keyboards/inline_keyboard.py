# keyboards/inline_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboard:
    def create_inline_markup(self, buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        
        for row in buttons:
            markup.row(*[InlineKeyboardButton(
                text=button[0],
                callback_data=button[1]
            ) for button in row])
            
        return markup

    # Інші методи...
