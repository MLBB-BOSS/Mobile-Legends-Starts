from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def handle_start_command(message: Message):
    logger.info("Отримано команду /start")
    from keyboards.menus import MainMenu
    keyboard = MainMenu.get_main_menu()
    await message.answer("Вітаю! Це головне меню:", reply_markup=keyboard)

@router.message(Command("help"))
async def handle_help_command(message: Message):
    logger.info("Отримано команду /help")
    await message.answer("Довідка: цей бот дозволяє ... (інструкції тут).")
