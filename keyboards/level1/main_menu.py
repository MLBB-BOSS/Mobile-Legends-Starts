from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """
    Створює клавіатуру головного меню.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація")],
            [KeyboardButton(text="🪪 Профіль")]
        ],
        resize_keyboard=True  # Зменшує розмір кнопок
    )
