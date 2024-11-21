# File: keyboards/base_keyboard.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

class BaseKeyboard:
    @staticmethod
    def create_keyboard(buttons: List[str], row_width: int = 3) -> ReplyKeyboardMarkup:
        """
        Create a keyboard with specified buttons and row width
        
        Args:
            buttons: List of button texts
            row_width: Number of buttons in each row (default 3)
            
        Returns:
            ReplyKeyboardMarkup with arranged buttons
        """
        keyboard = []
        row = []
        
        for button in buttons:
            row.append(KeyboardButton(text=button))
            if len(row) == row_width:
                keyboard.append(row)
                row = []
                
        if row:  # Add any remaining buttons
            keyboard.append(row)
            
        # Add back button in a separate row
        keyboard.append([KeyboardButton(text="↩️ Назад")])
        
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )
