from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class NavigationMenu:
    def get_builds_menu(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.build1")),
                    KeyboardButton(text=loc.get_message("buttons.build2"))
                ],
                [
                    KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard

    # Existing methods...
