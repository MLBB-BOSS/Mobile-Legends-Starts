# keyboards/base_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

class BaseKeyboard:
    def __init__(self):
        self._current_level = None

    def create_keyboard(
        self,
        buttons: List[List[str]],
        add_back: bool = True,
        add_main: bool = True
    ) -> ReplyKeyboardMarkup:
        keyboard = []
        
        # Додаємо основні кнопки
        for row in buttons:
            keyboard.append([KeyboardButton(text=str(btn)) for btn in row])
        
        # Додаємо навігаційні кнопки
        nav_row = []
        if add_back and self._current_level != MenuLevel.MAIN:
            nav_row.append(KeyboardButton(text=Buttons.BACK))
        if add_main and self._current_level != MenuLevel.MAIN:
            nav_row.append(KeyboardButton(text=Buttons.MAIN_MENU))
        
        if nav_row:
            keyboard.append(nav_row)
            
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
