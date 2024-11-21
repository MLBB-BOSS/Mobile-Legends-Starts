# handlers/start_command.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.navigation_keyboard import NavigationKeyboard
import logging

logger = logging.getLogger(__name__)
router = Router()
kb = NavigationKeyboard()

@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        await message.answer(
            "Вітаю! Я MLBB-BOSS бот.\nОберіть опцію з меню:",
            reply_markup=kb.get_main_menu()
        )
    except Exception as e:
        logger.error(f"Error processing start command: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
