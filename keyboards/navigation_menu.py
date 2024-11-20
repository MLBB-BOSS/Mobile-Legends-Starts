# File: keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc

class NavigationMenu:
    @staticmethod
    def get_main_navigation() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.guides")),
                    KeyboardButton(text=loc.get_message("buttons.characters"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.counter_picks")),
                    KeyboardButton(text=loc.get_message("buttons.builds"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.voting")),
                    KeyboardButton(text=loc.get_message("buttons.back"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def get_heroes_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.tanks")),
                    KeyboardButton(text=loc.get_message("buttons.fighters"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.assassins")),
                    KeyboardButton(text=loc.get_message("buttons.mages"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.marksmen")),
                    KeyboardButton(text=loc.get_message("buttons.supports"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def get_guides_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def get_counter_picks_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def get_builds_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def get_voting_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
