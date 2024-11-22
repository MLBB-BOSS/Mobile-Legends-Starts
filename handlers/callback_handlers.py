from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class NavigationMenu:
    @staticmethod
    def get_navigation_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Option 1", callback_data="option_1"))
        markup.add(InlineKeyboardButton(text="Option 2", callback_data="option_2"))
        return markup
