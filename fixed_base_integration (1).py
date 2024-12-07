
import logging
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardMarkup

from menus import (
    get_main_menu, get_profile_menu
)

# Logger
logger = logging.getLogger(__name__)

# Handlers

async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    logger.info(f"Main menu button pressed: {text}")
    if text == "🪪 Профіль":
        await message.answer("Перехід до профілю...", reply_markup=get_profile_menu())

async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    logger.info(f"Profile menu button pressed: {text}")
    if text == "📈 Статистика":
        await message.answer("Показ статистики...", reply_markup=ReplyKeyboardMarkup())
    elif text == MenuButton.BACK.value:
        await message.answer("Повернення до головного меню...", reply_markup=get_main_menu())
