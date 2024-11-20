# handlers/start_command.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.menu import get_main_menu_keyboard
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        welcome_text = loc.get_message("messages.start_command")
        keyboard = get_main_menu_keyboard()
        
        await message.answer(
            text=welcome_text,
            reply_markup=keyboard
        )
        logger.info(f"Користувач {message.from_user.id} запустив бота")
        
    except Exception as e:
        logger.error(f"Помилка в команді start: {e}")
        await message.answer(
            text=loc.get_message("errors.general")
        )
