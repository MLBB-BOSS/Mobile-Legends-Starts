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
            reply_markup=NavigationMenu().get_main_navigation()  # Змінено метод
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

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
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.back"))
async def handle_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    try:
        await message.answer(
            loc.get_message("messages.menu_welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до головного меню: {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message(F.text == loc.get_message("buttons.back_to_navigation"))
async def back_to_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_main_navigation()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.statistics"))
async def show_statistics(message: Message):
    logger.info(f"Користувач {message.from_user.id} переглядає статистику")
    try:
        stats = {
            "games": 0,
            "wins": 0,
            "winrate": 0
        }
        await message.answer(
            loc.get_message("messages.statistics_info").format(
                games=stats["games"],
                wins=stats["wins"],
                winrate=stats["winrate"]
            ),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні статистики: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.achievements"))
async def show_achievements(message: Message):
    logger.info(f"Користувач {message.from_user.id} переглядає досягнення")
    try:
        await message.answer(
            loc.get_message("messages.achievements_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при відображенні досягнень: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
