from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру головного меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Почати", callback_data="start")],
            [InlineKeyboardButton(text="Налаштування", callback_data="settings")],
            [InlineKeyboardButton(text="Допомога", callback_data="help")]
        ]
    )
