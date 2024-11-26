# keyboards/characters_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .main_menu import create_buttons, create_keyboard

def get_characters_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🗡️ Бійці", "🏹 Стрільці", "🔮 Маги"],
        ["🛡️ Танки", "🏥 Саппорти", "⚔️ Гібриди"],
        ["🔥 Метові"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть тип героя")
