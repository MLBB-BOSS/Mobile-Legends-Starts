from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_keyboard() -> InlineKeyboardMarkup:
    """
    Створює стандартну клавіатуру з кнопкою "Повернутися".
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Повернутися", callback_data="menu_back")]
    ])

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")]
    ])
