# handlers/main_menu.py
from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Ласкаво просимо до Mobile Legends Tournament Bot!\nОберіть опцію:",
        reply_markup=get_main_keyboard()
    )
