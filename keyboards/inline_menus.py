from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для першої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_1")
        ]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для другої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_2")
        ]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для третьої сторінки вступу з кнопкою 'Розпочати'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Розпочати", callback_data="intro_start")
        ]
    ])

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою '---MLS---'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data="mls_button")
        ]
    ])
