# File: handlers/start_command.py

from aiogram import Router, types
from aiogram.filters import Command
from keyboards.navigation_menu import NavigationMenu
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

router = Router()
nav_menu = NavigationMenu()
main_menu = MainMenu()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            text=loc.get_message("messages.welcome"),
            reply_markup=main_menu.get_main_menu()
        )
        logger.info(f"User {message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.answer(loc.get_message("errors.general"))
