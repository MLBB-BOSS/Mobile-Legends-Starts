from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """
    Створює головну клавіатуру з двома горизонтальними кнопками.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Профіль")],
        ],
        resize_keyboard=True  # Робить кнопки компактнішими
    )
