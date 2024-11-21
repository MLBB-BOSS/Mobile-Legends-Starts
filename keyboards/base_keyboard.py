# File: keyboards/base_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class BaseKeyboard:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()
    
    def create_markup(self, buttons: list, row_width: int = 2) -> ReplyKeyboardMarkup:
        """Create keyboard markup with specified buttons and row width"""
        self.builder.clear()
        
        # Add buttons in rows
        for i in range(0, len(buttons), row_width):
            row_buttons = buttons[i:i + row_width]
            self.builder.row(*[KeyboardButton(text=btn) for btn in row_buttons])
            
        return self.builder.as_markup(resize_keyboard=True)
