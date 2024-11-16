# File: keyboards/base.py
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from typing import List, Union, Dict

class BaseKeyboard:
    @staticmethod
    def create_keyboard(
        buttons: List[Union[str, Dict[str, str]]],
        row_width: int = 2,
        resize_keyboard: bool = True,
        **kwargs
    ) -> ReplyKeyboardMarkup:
        """
        Створює клавіатуру на основі списку кнопок
        
        :param buttons: Список кнопок
        :param row_width: Кількість кнопок в ряду (за замовчуванням 2)
        :param resize_keyboard: Чи змінювати розмір клавіатури
        :return: Об'єкт клавіатури
        """
        # Конвертуємо кнопки в об'єкти KeyboardButton
        button_objects = []
        for button in buttons:
            if isinstance(button, str):
                button_objects.append(KeyboardButton(text=button))
            elif isinstance(button, dict):
                button_objects.append(KeyboardButton(**button))
            else:
                button_objects.append(button)
        
        # Створюємо розмітку клавіатури
        keyboard_markup = []
        for i in range(0, len(button_objects), row_width):
            keyboard_markup.append(button_objects[i:i + row_width])
        
        # Створюємо клавіатуру з розміткою
        return ReplyKeyboardMarkup(
            keyboard=keyboard_markup,
            resize_keyboard=resize_keyboard,
            **kwargs
        )
