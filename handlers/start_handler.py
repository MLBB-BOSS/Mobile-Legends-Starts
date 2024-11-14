# handlers/start_handler.py

from aiogram import types, Dispatcher

# Створення Reply Keyboard з кнопками
def get_main_reply_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📜 Список героїв")
    keyboard.add("⚔️ Порівняння героїв", "🎯 Контргерої")
    keyboard.add("Назад")
    return keyboard

# Реєстрація обробника для команди /start
async def start_command(message: types.Message):
    await message.answer(
        "Вітаю! Я ваш бот, готовий допомогти.",
        reply_markup=get_main_reply_keyboard()
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
