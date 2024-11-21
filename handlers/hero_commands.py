# File: handlers/hero_commands.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.hero_menu import HeroMenu
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} запросив класи героїв")
    try:
        keyboard = HeroMenu().get_hero_classes_menu()
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Помилка при показі класів героїв: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
