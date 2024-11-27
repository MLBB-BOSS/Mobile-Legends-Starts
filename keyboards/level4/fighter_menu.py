from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_fighter_menu():
    """
    Створює меню для класу Fighter.
    :return: ReplyKeyboardMarkup
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Balmond"), KeyboardButton(text="Alucard"), KeyboardButton(text="Bane")],
            [KeyboardButton(text="Zilong"), KeyboardButton(text="Freya"), KeyboardButton(text="Alpha")],
            [KeyboardButton(text="🔄 Назад")],
        ],
        resize_keyboard=True
    )
