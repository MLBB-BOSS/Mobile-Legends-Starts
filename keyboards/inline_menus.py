from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(str, Enum):
    HEROES = "heroes"
    GUIDES = "guides"
    BACK = "back"

def get_generic_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="MLS Button", callback_data="mls_button")],
            [InlineKeyboardButton(text="Назад до меню", callback_data="menu_back")],
        ]
    )
    return keyboard

def get_intro_page_1_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard

def get_main_inline_keyboard():
    # Інлайн-клавіатура для головного меню (приклад)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Персонажі", callback_data=CallbackData.HEROES.value)],
            [InlineKeyboardButton(text="Гайди", callback_data=CallbackData.GUIDES.value)],
            [InlineKeyboardButton(text="Назад", callback_data=CallbackData.BACK.value)]
        ]
    )

def get_heroes_inline_keyboard():
    # Інлайн-клавіатура для меню героїв
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Список Героїв", callback_data="heroes_list")],
            [InlineKeyboardButton(text="Назад", callback_data=CallbackData.BACK.value)]
        ]
    )

def get_guides_inline_keyboard():
    # Інлайн-клавіатура для меню гайдів
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Нові гайди", callback_data="new_guides")],
            [InlineKeyboardButton(text="Назад", callback_data=CallbackData.BACK.value)]
        ]
    )
