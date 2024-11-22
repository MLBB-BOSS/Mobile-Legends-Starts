from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BaseKeyboard:
    """
    Базовий клас для створення InlineKeyboardMarkup з кнопками.
    """
    @staticmethod
    def create_inline_keyboard(buttons: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        """
        Створює клавіатуру з переданими кнопками.

        :param buttons: Двовимірний список кнопок (InlineKeyboardButton).
        :return: InlineKeyboardMarkup з заданими кнопками.
        """
        return InlineKeyboardMarkup(inline_keyboard=buttons)
