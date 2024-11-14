# handlers/start_handler.py

from aiogram import types
from aiogram.dispatcher import Dispatcher

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])

async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Герої"))
    keyboard.add(types.KeyboardButton("Таблиця лідерів"), types.KeyboardButton("Профіль"))
    await message.answer("Вітаю! Я ваш бот, готовий допомогти.", reply_markup=keyboard)
