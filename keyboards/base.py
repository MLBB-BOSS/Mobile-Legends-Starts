from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Union, Dict

class BaseKeyboard:
    @staticmethod
    def create_keyboard(
        buttons: List[List[Union[str, Dict[str, str]]]], 
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
            keyboard_row = []
            for button in row:
                if is_inline:
                    if isinstance(button, dict):
                        keyboard_row.append(InlineKeyboardButton(**button))
                    else:
                        keyboard_row.append(InlineKeyboardButton(text=button, callback_data=f"btn_{button}"))
                else:
                    keyboard_row.append(KeyboardButton(text=button))
            keyboard.append(keyboard_row)

        if is_inline:
            return InlineKeyboardMarkup(inline_keyboard=keyboard, **kwargs)
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=resize_keyboard, **kwargs)
