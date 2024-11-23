from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class StartMenu:
    """Клавіатура для стартової команди."""

    @staticmethod
    def get_start_menu() -> ReplyKeyboardMarkup:
        """
        Створює стартову клавіатуру з основними опціями.
        
        Returns:
            ReplyKeyboardMarkup: Клавіатура з основними опціями.
        """
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Профіль")],
                [KeyboardButton(text="📚 Довідка"), KeyboardButton(text="⚙️ Налаштування")],
            ],
            resize_keyboard=True
        )
