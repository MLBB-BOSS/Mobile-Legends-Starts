from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📩 Керувати повідомленнями", callback_data="manage_messages")
    builder.adjust(1)
    return builder.as_markup()
