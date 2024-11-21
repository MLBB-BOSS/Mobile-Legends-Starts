# File: keyboards/base.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List
from utils.localization import loc

class BaseKeyboard:
    @staticmethod
    def create_keyboard(
        button_keys: List[str], 
        row_width: int = 2, 
        add_back: bool = True,
        back_key: str = "buttons.back"
    ) -> ReplyKeyboardMarkup:
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
            back_text = loc.get_message(back_key)
            keyboard.append([KeyboardButton(text=back_text)])
            
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )
