from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    @staticmethod
    def get_main_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Навігація"), KeyboardButton(text="Профіль")]
            ],
            resize_keyboard=True
        )
