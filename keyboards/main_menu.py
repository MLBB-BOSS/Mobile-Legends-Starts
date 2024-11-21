from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenuKeyboard:
    """
    Клас для створення головної клавіатури
    """
    @staticmethod
    def get_keyboard() -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text="🧭 Навігація")],
            [KeyboardButton(text="🪪 Профіль")]
        ]
        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )
