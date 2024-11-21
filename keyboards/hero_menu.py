# keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import LocalizationManager

class HeroMenu:
    def __init__(self, locale: str = "uk"):
        self.loc = LocalizationManager(locale=locale)

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(self.loc.get_message("buttons.tanks"))],
            [KeyboardButton(self.loc.get_message("buttons.fighters"))],
            [KeyboardButton(self.loc.get_message("buttons.assassins"))],
            [KeyboardButton(self.loc.get_message("buttons.mages"))],
            [KeyboardButton(self.loc.get_message("buttons.marksmen"))],
            [KeyboardButton(self.loc.get_message("buttons.supports"))],
            [KeyboardButton(self.loc.get_message("buttons.back_to_navigation"))]
        ]
        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )

    def get_heroes_by_class(self, class_name: str) -> ReplyKeyboardMarkup:
        heroes = self._get_heroes_for_class(class_name)
        buttons = [[KeyboardButton(hero)] for hero in heroes]
        buttons.append([KeyboardButton(self.loc.get_message("buttons.back_to_hero_classes"))])
        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )

    def _get_heroes_for_class(self, class_name: str) -> list:
        # Fetch heroes from localization data
        try:
            heroes = self.loc.messages.get("heroes", {}).get("classes", {}).get(class_name.lower(), {}).get("heroes", [])
            return heroes
        except Exception as e:
            logger.error(f"Error fetching heroes for class {class_name}: {e}")
            return []
