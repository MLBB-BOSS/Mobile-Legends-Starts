from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Мій профіль")],
                [KeyboardButton(text="🔄 Назад")]
            ],
            resize_keyboard=True
        )
        return keyboard

class NavigationMenu:
    @staticmethod
    def get_navigation_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Місця"), KeyboardButton(text="Події")],
                [KeyboardButton(text="🔄 Назад")]
            ],
            resize_keyboard=True
        )
        return keyboard

class SubMenu:
    @staticmethod
    def get_sub_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔄 Назад")]
            ],
            resize_keyboard=True
        )
        return keyboard

class ProfileMenu:
    @staticmethod
    def get_profile_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Налаштування")],
                [KeyboardButton(text="🔄 Назад")]
            ],
            resize_keyboard=True
        )
        return keyboard
