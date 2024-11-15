from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hlink
import logging

logger = logging.getLogger(__name__)

router = Router(name="main_router")  # Додаємо name для кращого логування

@router.message(CommandStart())  # Використовуємо CommandStart замість Command("start")
async def start_command(message: Message):
    """Відповідає на команду /start."""
    logger.info(f"Користувач {message.from_user.id} запустив бота.")
    await message.answer("Ласкаво просимо до бота Mobile Legends!")

@router.message(Command("help"))
async def help_command(message: Message):
    """Відповідає на команду /help."""
    logger.info(f"Користувач {message.from_user.id} запитав допомогу.")
    help_text = (
        "📖 Допомога\n\n"
        "/start - Запустити бота\n"
        "/help - Отримати допомогу\n"
        "/screenshots - Переглянути скріншоти\n"
        "/leaderboard - Таблиця лідерів\n"
        "/profile - Ваш профіль"
    )
    await message.answer(help_text)

@router.message(Command("hero_info"))
async def hero_info_command(message: Message):
    """Відповідає на команду /hero_info."""
    logger.info(f"Користувач {message.from_user.id} запитав інформацію про героя.")
    await message.answer("Інформація про героя!")

@router.message(Command("info"))
async def info_command(message: Message):
    """Відповідає на команду /info з загальною інформацією."""
    logger.info(f"Користувач {message.from_user.id} запитав загальну інформацію.")
    await message.answer("Загальна інформація про бота Mobile Legends.")

@router.message(Command("leaderboard"))
async def leaderboard_command(message: Message):
    """Відповідає з таблицею лідерів."""
    logger.info(f"Користувач {message.from_user.id} запитав таблицю лідерів.")
    await message.answer("Таблиця лідерів: інформація буде додана.")

@router.message(Command("profile"))
async def profile_command(message: Message):
    """Відповідає з інформацією профілю користувача."""
    logger.info(f"Користувач {message.from_user.id} запитав профіль.")
    await message.answer("Ваш профіль: інформація буде додана.")

@router.message(Command("screenshots"))
async def screenshots_command(message: Message):
    """Відповідає з посиланням на скріншоти."""
    logger.info(f"Користувач {message.from_user.id} запитав скріншоти.")
    screenshots_link = hlink("Скріншоти", "https://example.com/screenshots")
    await message.answer(f"Перегляньте скріншоти тут: {screenshots_link}")

@router.message(F.text)  # Використовуємо F.text замість звичайного message()
async def unknown_command(message: Message):
    """Обробляє невідомі команди."""
    logger.warning(f"Користувач {message.from_user.id} ввів невідому команду: {message.text}")
    await message.answer("Вибачте, я не розумію цю команду. Спробуйте /help для отримання списку доступних команд.")
