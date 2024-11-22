# handlers/start_command.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.start_command import StartMenu
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "/start")
async def handle_start_command(message: Message):
    logger.info("Отримано команду /start")
    keyboard = StartMenu.get_start_menu()
    await message.answer("Вітаємо! Оберіть опцію:", reply_markup=keyboard)
