from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .main_menu import create_buttons, create_keyboard

def get_mp3_player_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["▶️ Відтворити", "⏸️ Пауза", "⏹️ Стоп"],
        ["⏭️ Наступний трек", "⏮️ Попередній трек"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)
