from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_navigation_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message(F.text == loc.get_message("buttons.profile"))
async def show_profile(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив особистий кабінет")
    try:
        await message.answer(
            loc.get_message("messages.profile_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні особистого кабінету: {e}")
        await message.answer(loc.get_message("errors.general"))
