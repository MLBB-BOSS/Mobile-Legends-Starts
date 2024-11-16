# File: keyboards/base.py
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from typing import List, Union, Dict
from .utils import create_keyboard_row

class BaseKeyboard:
    @staticmethod
    def create_keyboard(
        buttons: List[List[Union[str, Dict[str, str], InlineKeyboardButton]]], 
        is_inline: bool = False,
        resize_keyboard: bool = True,
        **kwargs
    ) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        """
        Створює клавіатуру на основі списку кнопок
        
        :param buttons: Список списків з текстом кнопок або словників для inline кнопок
        :param is_inline: Чи створювати inline клавіатуру
        :param resize_keyboard: Чи змінювати розмір клавіатури
        :return: Об'єкт клавіатури
        """
        keyboard = []
        for row in buttons:
            if is_inline:
                keyboard_row = create_keyboard_row(*row)
            else:
                keyboard_row = [KeyboardButton(text=button) if isinstance(button, str) 
                              else KeyboardButton(**button) for button in row]
            keyboard.append(keyboard_row)

        if is_inline:
            return InlineKeyboardMarkup(inline_keyboard=keyboard, **kwargs)
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=resize_keyboard, **kwargs)

    @classmethod
    def create_row(cls, *buttons: Union[Dict, InlineKeyboardButton]) -> List[InlineKeyboardButton]:
        """
        Створює ряд inline кнопок
        
        :param buttons: Кнопки у вигляді словників або об'єктів InlineKeyboardButton
        :return: Список кнопок InlineKeyboardButton
        """
        return create_keyboard_row(*buttons)
