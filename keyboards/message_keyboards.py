from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_message_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✉️ Надіслати повідомлення", callback_data="send_message")
    builder.button(text="🗑 Видалити повідомлення", callback_data="delete_message")
    builder.button(text="✏️ Змінити повідомлення", callback_data="edit_message")
    builder.button(text="⬅️ Назад", callback_data="start_menu")
    builder.adjust(1)
    return builder.as_markup()
