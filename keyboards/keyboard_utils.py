# File: keyboards/keyboard_utils.py
from aiogram.types import InlineKeyboardButton
from typing import List, Union, Dict

def create_keyboard_row(*buttons: Union[Dict, InlineKeyboardButton]) -> List[InlineKeyboardButton]:
    """
    Створює ряд кнопок з словників або готових кнопок
    
    :param buttons: Кнопки у вигляді словників або об'єктів InlineKeyboardButton
    :return: Список кнопок InlineKeyboardButton
    """
    row = []
    for button in buttons:
        if isinstance(button, dict):
            row.append(InlineKeyboardButton(**button))
        elif isinstance(button, InlineKeyboardButton):
            row.append(button)
    return row
