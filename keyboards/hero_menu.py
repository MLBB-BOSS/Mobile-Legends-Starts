# keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import LocalizationManager
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    def __init__(self, locale: str = "uk"):
        self.loc = LocalizationManager(locale=locale)

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        try:
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
        except Exception as e:
            logger.exception(f"Error generating heroes menu: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[],
                resize_keyboard=True,
                one_time_keyboard=True
            )

    def get_heroes_by_class(self, class_name: str) -> ReplyKeyboardMarkup:
        try:
            heroes = self._get_heroes_for_class(class_name)
            if not heroes:
                return ReplyKeyboardMarkup(
                    keyboard=[],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            buttons = [[KeyboardButton(hero)] for hero in heroes]
            buttons.append([KeyboardButton(self.loc.get_message("buttons.back_to_hero_classes"))])
            return ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        except Exception as e:
            logger.exception(f"Error generating heroes by class menu: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[],
                resize_keyboard=True,
                one_time_keyboard=True
            )

    def _get_heroes_for_class(self, class_name: str) -> list:
        try:
            heroes = self.loc.messages.get("heroes", {}).get("classes", {}).get(class_name, {}).get("heroes", [])
            return heroes
        except Exception as e:
            logger.error(f"Error fetching heroes for class {class_name}: {e}")
            return []
