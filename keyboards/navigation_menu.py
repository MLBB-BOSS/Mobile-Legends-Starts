from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def navigation_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Опція 1"),
        KeyboardButton("Опція 2")
    )
    keyboard.add(KeyboardButton("Повернутися до головного меню"))
    return keyboard
