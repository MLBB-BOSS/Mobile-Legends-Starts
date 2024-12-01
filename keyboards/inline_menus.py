from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_intro_keyboard(page: int) -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для сторінок вступу.
    :param page: Номер сторінки (1, 2, 3).
    :return: InlineKeyboardMarkup для відповідної сторінки.
    """
    buttons = {
        1: [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        2: [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        3: [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")]
    }
    if page in buttons:
        return InlineKeyboardMarkup(inline_keyboard=[buttons[page]])
    else:
        raise ValueError("Invalid page number. Supported pages: 1, 2, 3.")

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для головного меню.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Головне меню", callback_data="main_menu_back")
        ]
    ])

def get_generic_keyboard(button_text: str, callback_data: str) -> InlineKeyboardMarkup:
    """
    Створює універсальну інлайн-клавіатуру з однією кнопкою.
    :param button_text: Текст кнопки.
    :param callback_data: Callback дані для кнопки.
    :return: InlineKeyboardMarkup
    """
    if not button_text or not callback_data:
        raise ValueError("Both button_text and callback_data must be provided.")
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        ]
    ])
