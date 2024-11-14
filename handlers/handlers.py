# handlers/handlers.py

from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from services.screenshot_service import get_hero_info

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    await message.reply("Вітаю! Я ваш бот, готовий допомогти.")

@router.message(commands=["help"])
async def help_command(message: Message):
    await message.reply("📖 Допомога\n\n"
                        "/start - Запустити бота\n"
                        "/help - Отримати допомогу\n"
                        "/screenshots - Переглянути скріншоти\n"
                        "/leaderboard - Таблиця лідерів\n"
                        "/profile - Ваш профіль")

@router.message(commands=["hero_info"])
async def hero_info_command(message: Message):
    await message.reply("Інформація про героя!")

@router.message(commands=["info"])
async def info_command(message: Message):
    await message.reply("Це загальна інформація!")

@router.message(commands=["leaderboard"])
async def leaderboard_command(message: Message):
    await message.reply("Тут буде таблиця лідерів.")

@router.message(commands=["profile"])
async def profile_command(message: Message):
    await message.reply("Ваш профіль!")

@router.message(commands=["screenshots"])
async def screenshots_command(message: Message):
    try:
        hero_info = get_hero_info()
        await message.reply(f"Скріншоти: {hero_info}")
    except Exception as e:
        await message.reply("❌ Виникла помилка при отриманні скріншотів.")
        print(f"Error in screenshots_command: {e}")

@router.callback_query()
async def handle_callback(call: CallbackQuery):
    try:
        await call.answer("Це тестове повідомлення для callback!")
    except Exception as e:
        await call.message.reply("❌ Виникла помилка при обробці callback.")
        print(f"Error in handle_callback: {e}")
