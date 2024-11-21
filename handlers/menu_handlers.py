import logging
from aiogram import Router, types
from aiogram.filters import Text
from utils.localization import loc
from keyboards.main_menu import MainMenu
from keyboards.hero_menu import HeroMenu

logger = logging.getLogger(__name__)
router = Router()

@router.message(Text(text=loc.get_message("buttons.show_heroes")))
async def show_heroes(message: types.Message):
    try:
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=HeroMenu().get_hero_classes_menu()
        )
        logger.info(f"User {message.from_user.id} requested to show heroes.")
    except Exception as e:
        logger.exception(f"Error in show_heroes handler: {e}")
        await message.answer(
            loc.get_message("messages.errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
