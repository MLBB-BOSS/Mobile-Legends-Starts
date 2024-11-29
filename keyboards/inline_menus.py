# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою '---MLS---'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data="mls_button")
        ]
    ])

def get_welcome_keyboard(page: int) -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для привітального процесу.
    """
    if page == 1:
        buttons = [
            InlineKeyboardButton(text="Продовжити", callback_data="welcome_continue_1")
        ]
    elif page == 2:
        buttons = [
            InlineKeyboardButton(text="Продовжити", callback_data="welcome_continue_2")
        ]
    elif page == 3:
        buttons = [
            InlineKeyboardButton(text="Розпочати", callback_data="welcome_start")
        ]
    else:
        buttons = []
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard
