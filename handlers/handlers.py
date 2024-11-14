# handlers/handlers.py
from aiogram import F, Router
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    """Відповідає на команду /start."""
    await message.reply("Ласкаво просимо до бота Mobile Legends!")

@router.message(F.text == "/help")
async def help_command(message: Message):
    await message.reply("📖 Допомога\n\n"
                        "/start - Запустити бота\n"
                        "/help - Отримати допомогу\n"
                        "/screenshots - Переглянути скріншоти\n"
                        "/leaderboard - Таблиця лідерів\n"
                        "/profile - Ваш профіль")

@router.message(F.text == "/hero_info")
async def hero_info_command(message: Message):
    await message.reply("Інформація про героя!")

@router.message(F.text == "/info")
async def info_command(message: Message):
    """Відповідає на команду /info з загальною інформацією."""
    await message.reply("Загальна інформація про бота Mobile Legends.")

@router.message(F.text == "/leaderboard")
async def leaderboard_command(message: Message):
    """Відповідає з таблицею лідерів."""
    await message.reply("Таблиця лідерів: інформація буде додана.")

@router.message(F.text == "/profile")
async def profile_command(message: Message):
    """Відповідає з інформацією профілю користувача."""
    await message.reply("Ваш профіль: інформація буде додана.")

@router.message(F.text == "/screenshots")
async def screenshots_command(message: Message):
    """Відповідає з посиланням на скріншоти."""
    await message.reply("Перегляньте скріншоти тут: [посилання]")
