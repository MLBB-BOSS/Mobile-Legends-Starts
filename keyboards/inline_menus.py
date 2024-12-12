from aiogram.dispatcher.filters.callback_data import CallbackData  # Оновлений імпорт
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Визначення CallbackData
callback_data = CallbackData("action", "page")

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data=callback_data.new(action="intro_next", page=1))
        ]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data=callback_data.new(action="intro_next", page=2))
        ]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Розпочати", callback_data=callback_data.new(action="intro_start", page=3))
        ]
    ])

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data=callback_data.new(action="mls_button", page=0))
        ]
    ])

def get_guides_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Нові Гайди", callback_data=callback_data.new(action="guides_new", page=1)),
            InlineKeyboardButton(text="Популярні Гайди", callback_data=callback_data.new(action="guides_popular", page=1))
        ],
        [
            InlineKeyboardButton(text="Для Початківців", callback_data=callback_data.new(action="guides_beginner", page=1)),
            InlineKeyboardButton(text="Стратегії гри", callback_data=callback_data.new(action="guides_advanced", page=1))
        ],
        [
            InlineKeyboardButton(text="Командна Гра", callback_data=callback_data.new(action="guides_teamplay", page=1))
        ]
    ])