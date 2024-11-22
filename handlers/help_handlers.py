# handlers/help_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.help_menu import HelpMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "/help")
async def handle_help(message: Message):
    logger.info("Отримано команду /help")
    keyboard = HelpMenu.get_help_menu()
    await message.answer("Довідка:", reply_markup=keyboard)
