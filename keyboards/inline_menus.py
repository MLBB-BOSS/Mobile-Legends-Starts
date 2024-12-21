from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(str, Enum):
    HEROES = "heroes"
    GUIDES = "guides"
    BACK = "back"

def get_generic_inline_keyboard():
    """
    Видаляємо усі інлайн-кнопки, окрім тих, що вам можуть бути потрібні
    — але зараз залишаємо лише «порожнє» або мінімальне інлайн-повідомлення.
    Приклад — абсолютно без кнопок.
    """
    # Порожнє інлайн-меню, або мінімальний варіант
    # Залишаємо None або створюємо «порожнє» InlineKeyboardMarkup
    # Якщо треба взагалі без кнопок — можна повернути None.
    return None

def get_intro_page_1_keyboard():
    """
    Кнопки для сторінок інтро залишаємо.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard():
    """
    Кнопки для сторінок інтро залишаємо.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard():
    """
    Кнопки для сторінок інтро залишаємо.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard

########################
# Приклад "головного" інлайн-меню та інших функцій нижче видаляємо або робимо порожніми,
# бо за умовою треба прибрати усі інлайн-кнопки (крім інтро).
########################

def get_main_inline_keyboard():
    """
    Раніше тут була інлайн-клавіатура з 3 кнопками.
    Тепер робимо «порожньою» або повертаємо None.
    """
    return None

def get_heroes_inline_keyboard():
    """
    Раніше тут була інлайн-клавіатура для «Герої».
    Прибираємо кнопки.
    """
    return None

def get_guides_inline_keyboard():
    """
    Раніше тут була інлайн-клавіатура для «Гайди».
    Прибираємо кнопки.
    """
    return None