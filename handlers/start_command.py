# handlers/start_command.py

import logging
from aiogram import Router, F
from aiogram.types import Message
from keyboards.start_command import StartMenu  # Імпортуємо StartMenu замість router

logger = logging.getLogger(__name__)

# Створення екземпляра Router
router = Router()

@router.message(commands=["start"])  # Більш стандартний спосіб обробки команд
async def handle_start_command(message: Message):
    start_menu = StartMenu.get_start_menu()
    await message.answer("Вітаю! Це стартова команда.", reply_markup=start_menu)
