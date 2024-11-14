# services/keyboard_service.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_class_keyboard():
    """Повертає клавіатуру для вибору класу героїв."""
    keyboard = InlineKeyboardMarkup()
    classes = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank"]
    for hero_class in classes:
        keyboard.add(InlineKeyboardButton(text=hero_class, callback_data=f"class_{hero_class}"))
    return keyboard

def get_heroes_keyboard(hero_class):
    """Повертає клавіатуру для вибору героя з певного класу."""
    keyboard = InlineKeyboardMarkup()
    # Список героїв для кожного класу може бути збережений у файлах або базі даних
    heroes = ["Hero1", "Hero2", "Hero3"]  # Приклад героїв
    for hero in heroes:
        keyboard.add(InlineKeyboardButton(text=hero, callback_data=f"hero_{hero}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_classes"))
    return keyboard
