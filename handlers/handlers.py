# handlers/handlers.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    """Відповідає на команду /start."""
    await message.reply("Ласкаво просимо до бота Mobile Legends!")

@router.message(Command("help"))
async def help_command(message: Message):
    """Відповідає на команду /help."""
    await message.reply("📖 Допомога\n\n"
                        "/start - Запустити бота\n"
                        "/help - Отримати допомогу\n"
                        "/screenshots - Переглянути скріншоти\n"
                        "/leaderboard - Таблиця лідерів\n"
                        "/profile - Ваш профіль")

@router.message(Command("hero_info"))
async def hero_info_command(message: Message):
    """Відповідає на команду /hero_info."""
    await message.reply("Інформація про героя!")

@router.message(Command("info"))
async def info_command(message: Message):
    """Відповідає на команду /info з загальною інформацією."""
    await message.reply("Загальна інформація про бота Mobile Legends.")

@router.message(Command("leaderboard"))
async def leaderboard_command(message: Message):
    """Відповідає з таблицею лідерів."""
    await message.reply("Таблиця лідерів: інформація буде додана.")

@router.message(Command("profile"))
async def profile_command(message: Message):
    """Відповідає з інформацією профілю користувача."""
    await message.reply("Ваш профіль: інформація буде додана.")

@router.message(Command("screenshots"))
async def screenshots_command(message: Message):
    """Відповідає з посиланням на скріншоти."""
    await message.reply("Перегляньте скріншоти тут: <a href='https://example.com/screenshots'>Скріншоти</a>", parse_mode="HTML")

@router.message()
async def unknown_command(message: Message):
    """Обробляє невідомі команди."""
    await message.reply("Вибачте, я не розумію цю команду. Спробуйте /help для отримання списку доступних команд.")
