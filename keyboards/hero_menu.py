# File: keyboards/hero_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import loc

class HeroMenu:
    def get_hero_class_menu(self):
        keyboard = []
        hero_classes = loc.get_message("heroes.classes")
        for class_key, class_info in hero_classes.items():
            class_name = class_info["name"]
            button = InlineKeyboardButton(
                text=class_name,
                callback_data=f'hero_class_{class_key}'
            )
            keyboard.append([button])
        keyboard.append([
            InlineKeyboardButton(
                text=loc.get_message("buttons.back_to_navigation"),
                callback_data='back_to_navigation'
            )
        ])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def get_heroes_by_class(self, class_key):
        keyboard = []
        class_info = loc.get_message(f"heroes.classes.{class_key}")
        heroes = class_info.get("heroes", [])
        for hero_name in heroes:
            button = InlineKeyboardButton(
                text=hero_name,
                callback_data=f'hero_select_{hero_name}'
            )
            keyboard.append([button])
        keyboard.append([
            InlineKeyboardButton(
                text=loc.get_message("buttons.back_to_classes"),
                callback_data='back_to_hero_classes'
            )
        ])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def get_hero_details_menu(self, hero_id):
        keyboard = [
            [
                InlineKeyboardButton(
                    text=loc.get_message("buttons.back_to_hero_list"),
                    callback_data='back_to_hero_list'
                )
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
