# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.menus import MenuButton, heroes_by_class

def get_generic_inline_keyboard():
    """
    Створює інлайн-клавіатуру з загальними кнопками.
    Можете змінити текст та callback_data відповідно до вашої логіки.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Пошук героя", callback_data="search_hero"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="statistics"),
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data="back"),
        ]
    ])
    return keyboard

def get_hero_class_inline_keyboard(hero_class):
    """
    Створює інлайн-клавіатуру з героями певного класу.
    """
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [
        InlineKeyboardButton(text=hero, callback_data=f"hero:{hero}") for hero in heroes
    ]
    buttons.append(InlineKeyboardButton(text=MenuButton.BACK.value, callback_data="back"))
    
    # Організуємо кнопки по 3 в рядок
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[i:i+3] for i in range(0, len(buttons), 3)
    ])
    return keyboard

# Додайте інші функції для створення інлайн-кнопок відповідно до вашої логіки
