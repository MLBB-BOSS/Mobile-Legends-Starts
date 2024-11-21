# File: core/bot.py

from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

async def cmd_start(message: types.Message):
    """Обробник команди /start"""
    try:
        # Створення клавіатури
        keyboard = MainMenu().get_main_menu()

        await message.reply(
            loc.get_message("messages.welcome"),
            reply_markup=keyboard  # Додаємо клавіатуру тут
        )
        logger.info(f"Користувач {message.from_user.id} запустив бота")
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        await message.reply("Вибачте, сталася помилка. Спробуйте пізніше.")
