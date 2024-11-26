from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .main_menu import create_buttons, create_keyboard

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["📈 Статистика", "🏆 Досягнення", "💌 Зворотний Зв'язок"],
        ["⚙️ Налаштування", "❓ Допомога", "🔙 Назад до Головного"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію профілю")
