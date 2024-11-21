from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BaseKeyboard:
    @staticmethod
    def create_inline_keyboard(buttons: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=buttons)
