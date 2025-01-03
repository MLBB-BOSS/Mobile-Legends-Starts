# bot.py
import os
from aiogram import Bot, Dispatcher, executor, types
from utils.db import init_db, check_connection
from dotenv import load_dotenv

# Завантажте змінні середовища з .env файлу (для локальної розробки)
load_dotenv()

# Отримайте токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

# Ініціалізуйте базу даних
init_db()

# Створіть екземпляри бота та диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Я ваш бот.")

if __name__ == '__main__':
    if check_connection():
        executor.start_polling(dp, skip_updates=True)
    else:
        print("Не вдалося підключитися до бази даних.")
