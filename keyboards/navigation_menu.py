# File: keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class NavigationMenu:
    @staticmethod
    def get_main_navigation() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row(
            KeyboardButton(text=loc.get_message("buttons.guides")),
            KeyboardButton(text=loc.get_message("buttons.characters"))
        )
        keyboard.row(
            KeyboardButton(text=loc.get_message("buttons.counter_picks")),
            KeyboardButton(text=loc.get_message("buttons.builds"))
        )
        keyboard.row(
            KeyboardButton(text=loc.get_message("buttons.voting")),
            KeyboardButton(text=loc.get_message("buttons.back"))
        )
        return keyboard

    @staticmethod
    def get_guides_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
        )
        return keyboard

    @staticmethod
    def get_counter_picks_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
        )
        return keyboard

    @staticmethod
    def get_builds_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
        )
        return keyboard

    @staticmethod
    def get_voting_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
        )
        return keyboard
