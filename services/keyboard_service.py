# services/keyboard_service.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

def get_class_keyboard():
    """Повертає клавіатуру з кнопками класів персонажів."""
    keyboard = InlineKeyboardMarkup()
    classes = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank"]
    for hero_class in classes:
        keyboard.add(InlineKeyboardButton(text=hero_class, callback_data=f"class_{hero_class}"))
    return keyboard

def get_heroes_keyboard(hero_class):
    """Повертає клавіатуру з персонажами обраного класу."""
    keyboard = InlineKeyboardMarkup()
    class_path = f"heroes/{hero_class}"
    try:
        for hero_file in os.listdir(class_path):
            if hero_file.endswith(".json"):
                hero_name = hero_file.replace(".json", "").replace("_", " ").title()
                keyboard.add(InlineKeyboardButton(text=hero_name, callback_data=f"hero_{hero_name}"))
        keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_classes"))
    except FileNotFoundError:
        keyboard.add(InlineKeyboardButton(text="Немає даних про цей клас", callback_data="no_data"))
    return keyboard
