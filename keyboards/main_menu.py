from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MainMenuKeyboard:
    """
    Клас для створення головного меню
    """
    @staticmethod
    def get_keyboard() -> ReplyKeyboardMarkup:
        # Створюємо кнопки
        navigation_button = KeyboardButton(text="🧭 Навігація")
        profile_button = KeyboardButton(text="🪪 Профіль")

        # Розміщуємо кнопки в один рядок
        return ReplyKeyboardMarkup(
            keyboard=[
                [navigation_button, profile_button]
            ],
            resize_keyboard=True,  # Робимо клавіатуру компактною
            one_time_keyboard=False  # Клавіатура не зникає після вибору
        )
