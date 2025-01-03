# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from utils.db import init_db, check_connection
from dotenv import load_dotenv

# Завантажте змінні середовища з .env файлу (для локальної розробки)
load_dotenv()

# Отримайте токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

# Створіть екземпляри бота та диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Я ваш бот.")

async def main():
    await init_db()
    if await check_connection():
        # Запустіть диспетчер
        await dp.start_polling(bot)
    else:
        print("Не вдалося підключитися до бази даних.")

if __name__ == '__main__':
    asyncio.run(main())