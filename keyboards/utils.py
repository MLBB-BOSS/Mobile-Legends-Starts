# Шлях: keyboards/utils.py
# Цей файл містить допоміжні функції для створення кнопок клавіатури
from aiogram.types import InlineKeyboardButton
from typing import List, Union, Dict

def create_keyboard_row(*buttons: Union[Dict, InlineKeyboardButton]) -> List[InlineKeyboardButton]:
    """Створює ряд кнопок з словників або готових кнопок"""
    row = []
    for button in buttons:
        if isinstance(button, dict):
            row.append(InlineKeyboardButton(**button))
        elif isinstance(button, InlineKeyboardButton):
            row.append(button)
    return row
