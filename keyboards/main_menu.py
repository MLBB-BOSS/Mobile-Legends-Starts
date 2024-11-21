class MainMenuKeyboard:
    @staticmethod
    def get_main_menu():
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Профіль")]
            ],
            resize_keyboard=True
        )
