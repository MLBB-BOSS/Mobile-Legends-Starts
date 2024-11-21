# File: handlers/start_command.py

import logging
from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_keyboard import MainKeyboard
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle the /start command"""
    try:
        keyboard = MainKeyboard()
        await message.answer(
            text=loc.get_message("welcome"),
            reply_markup=keyboard.get_main_menu()
        )
        logger.info(f"Start command processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error processing start command: {e}")
        await message.answer(loc.get_message("error.general"))
