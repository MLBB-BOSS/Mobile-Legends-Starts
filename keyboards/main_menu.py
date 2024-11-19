# keyboards/main_menu.py
class MainMenu:
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=loc.get_message("buttons.navigation")),
                    KeyboardButton(text=loc.get_message("buttons.profile"))
                ]
            ],
            resize_keyboard=True
        )
        return keyboard
