# File: handlers/message_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.back_to_hero_classes"))
async def back_to_hero_classes(message: Message):
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_heroes_menu()
        )
    except Exception as e:
        logger.exception(f"Error in back_to_hero_classes handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.back_to_hero_list"))
async def back_to_hero_list(message: Message):
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_heroes_menu()
        )
    except Exception as e:
        logger.exception(f"Error in back_to_hero_list handler: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

# Register other handlers here...

@router.message()
async def unhandled_message(message: Message):
    logger.info(f"Received unhandled message: {message.text}")
    try:
        response_text = loc.get_message("messages.unhandled_message", message=message.text)
        await message.answer(
            response_text,
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Error sending message: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
