# handlers/basic_handlers.py
from aiogram import types
from core.bot import dp

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Вітаю! Я ваш бот, готовий допомогти.")
