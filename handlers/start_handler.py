# handlers/start_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher

# Створення клавіатури
def create_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🦸 Герої", "📊 Таблиця лідерів")
    keyboard.add("📷 Скріншоти", "📑 Інформація")
    return keyboard

# Оновлений обробник для команди /start
async def start_command(message: types.Message):
    keyboard = create_main_menu()
    await message.answer("Вітаю! Я ваш бот, готовий допомогти.", reply_markup=keyboard)

# Реєстрація обробника в Dispatcher
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
