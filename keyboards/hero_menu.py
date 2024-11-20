# keyboards/hero_menu.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import loc

class HeroMenu:
    def get_hero_class_menu(self):
        keyboard = InlineKeyboardMarkup(row_width=2)
        hero_classes = loc.get_message("heroes.classes")
        for class_key, class_info in hero_classes.items():
            class_name = class_info["name"]
            button = InlineKeyboardButton(
                text=class_name,
                callback_data=f'hero_class_{class_key}'
            )
            keyboard.insert(button)
        keyboard.add(InlineKeyboardButton(
            text=loc.get_message("buttons.back_to_navigation"),
            callback_data='back_to_navigation'
        ))
        return keyboard

    def get_heroes_by_class(self, class_key):
        keyboard = InlineKeyboardMarkup(row_width=2)
        class_info = loc.get_message(f"heroes.classes.{class_key}")
        heroes = class_info.get("heroes", [])
        for hero_name in heroes:
            button = InlineKeyboardButton(
                text=hero_name,
                callback_data=f'hero_select_{hero_name}'
            )
            keyboard.insert(button)
        keyboard.add(InlineKeyboardButton(
            text=loc.get_message("buttons.back_to_classes"),
            callback_data='back_to_hero_classes'
        ))
        return keyboard

    def get_hero_details_menu(self, hero_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            text=loc.get_message("buttons.back_to_hero_list"),
            callback_data='back_to_hero_list'
        ))
        return keyboard

    def get_class_from_hero(self, hero_id):
        hero_classes = loc.get_message("heroes.classes")
        for class_key, class_info in hero_classes.items():
            if hero_id in class_info.get("heroes", []):
                return class_key
        return None
