# File: keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class HeroMenu:
    @staticmethod
    def get_hero_class_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        hero_classes = loc.get_message("heroes.classes")
        for class_info in hero_classes.values():
            keyboard.add(KeyboardButton(text=class_info["name"]))
        keyboard.add(KeyboardButton(text=loc.get_message("buttons.back_to_navigation")))
        return keyboard

    @staticmethod
    def get_heroes_by_class(class_key) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        class_info = loc.get_message(f"heroes.classes.{class_key}")
        for hero_name in class_info["heroes"]:
            keyboard.add(KeyboardButton(text=hero_name))
        keyboard.add(KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes")))
        return keyboard

    @staticmethod
    def get_hero_details_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes")))
        return keyboard
