from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Створення CallbackData для обробки динамічних дій
intro_callback = CallbackData("intro", "page")  # Динамічний колбек для вступу
generic_callback = CallbackData("generic", "action")  # Для загальних дій

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для першої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data=intro_callback.new(page="2"))
        ]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для другої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data=intro_callback.new(page="3"))
        ]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для третьої сторінки вступу з кнопкою 'Розпочати'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Розпочати", callback_data=intro_callback.new(page="start"))
        ]
    ])

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою '---MLS---'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data=generic_callback.new(action="mls_button"))
        ]
    ])
