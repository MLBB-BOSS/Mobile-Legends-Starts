# keyboards/main_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_network_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_refresh = InlineKeyboardButton(text="🔄 Оновити Граф", callback_data="refresh_graph")
    button_help = InlineKeyboardButton(text="❓ Допомога", callback_data="help_network")
    keyboard.add(button_refresh, button_help)
    return keyboard
