# File: keyboards/base.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from typing import List, Optional
from utils.localization import loc

class BaseKeyboard:
    @staticmethod
    def create_keyboard(
        button_keys: List[str], 
        row_width: int = 3, 
        add_back: bool = True
    ) -> ReplyKeyboardMarkup:
        """
        Create keyboard with localized buttons
        
        Args:
            button_keys: List of localization keys for buttons
            row_width: Number of buttons per row
            add_back: Whether to add back button
        """
        keyboard = []
        row = []
        
        for key in button_keys:
            button_text = loc.get_message(key)
            row.append(KeyboardButton(text=button_text))
            if len(row) == row_width:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
            
        if add_back:
            back_text = loc.get_message("buttons.common.back")
            keyboard.append([KeyboardButton(text=back_text)])
            
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )

    @staticmethod
    def remove_keyboard() -> ReplyKeyboardRemove:
        """Remove current keyboard"""
        return ReplyKeyboardRemove()
