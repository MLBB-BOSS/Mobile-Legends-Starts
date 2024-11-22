# handlers/start_command.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.menus import get_main_menu
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

# Ініціалізація маршрутизатора
start_router = Router()

@start_router.message(F.text == "/start")
async def handle_start_command(message: Message):
    """
    Обробляє команду /start.
    """
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    keyboard = get_main_menu()
    await message.answer(
        "Вітаю! Це головне меню вашого бота.\nОберіть опцію:",
        reply_markup=keyboard
    )
