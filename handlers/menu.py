import logging
from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import get_main_menu
from keyboards.navigation_menu import get_navigation_menu

# Ініціалізація роутера
menu_router = Router()

# Налаштування логування
logger = logging.getLogger(__name__)

@menu_router.message(F.text == "/start")
async def show_main_menu(message: Message):
    """
    Показує головне меню.
    """
    logger.info(f"Користувач {message.from_user.id} викликав команду /start")
    await message.answer("Ласкаво просимо! Оберіть опцію:", reply_markup=get_main_menu())

@menu_router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    """
    Показує меню навігації.
    """
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    await message.answer("Оберіть розділ:", reply_markup=get_navigation_menu())
