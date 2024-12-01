from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_inline_keyboard(button_text="Назад", callback_data="menu_back") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, callback_data=callback_data)]
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
