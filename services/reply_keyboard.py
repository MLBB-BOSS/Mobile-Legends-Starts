from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="🎮 Герої"),
            KeyboardButton(text="📊 Статистика")
        ],
        [
            KeyboardButton(text="ℹ️ Інформація"),
            KeyboardButton(text="⚙️ Налаштування")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
