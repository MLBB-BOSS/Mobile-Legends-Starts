from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_menu():
    """
    Створює клавіатуру для навігації.

    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡️ Персонажі")],
            [KeyboardButton(text="📚 Гайди")],
            [KeyboardButton(text="⚖️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
            [KeyboardButton(text="📊 Голосування")],
            [KeyboardButton(text="🔄 Назад")]
        ],
        resize_keyboard=True
    )
