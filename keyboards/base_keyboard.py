# keyboards/base_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class BaseKeyboard:
    """Base class for all keyboards"""
    
    def create_reply_markup(
        self,
        keyboard: list[list[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )
        
        for row in keyboard:
            markup.row(*[KeyboardButton(text=button) for button in row])
            
        return markup
