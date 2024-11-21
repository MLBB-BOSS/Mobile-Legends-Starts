from aiogram import Router, F, types
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu
from keyboards.main_menu import MainMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization_instance import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

# Helper: Cache localized messages for buttons to avoid repeated lookups
BUTTONS = {
    "navigation": loc.get_message("buttons.navigation"),
    "characters": loc.get_message("buttons.characters"),
    "back": loc.get_message("buttons.back"),
    "back_to_navigation": loc.get_message("buttons.back_to_navigation"),
    "guides": loc.get_message("buttons.guides"),
    "counter_picks": loc.get_message("buttons.counter_picks"),
    "builds": loc.get_message("buttons.builds"),
    "voting": loc.get_message("buttons.voting"),
    "statistics": loc.get_message("buttons.statistics")
}

@router.message(F.text == BUTTONS["navigation"])
async def show_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_main_navigation()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == BUTTONS["characters"])
async def show_heroes(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню персонажів")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=NavigationMenu().get_heroes_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню персонажів: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == BUTTONS["back"])
async def handle_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    try:
        await message.answer(
            loc.get_message("messages.menu_welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до головного меню: {e}")
        await message.answer(
            loc.get_message("errors.general")
        )

@router.message(F.text == BUTTONS["statistics"])
async def show_statistics(message: Message):
    logger.info(f"Користувач {message.from_user.id} запросив статистику")
    try:
        # Fetch stats dynamically (replace with actual data retrieval)
        stats = {
            "games": 10,
            "wins": 7,
            "winrate": round((7 / 10) * 100, 2)
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
        logger.exception(f"Помилка при відображенні статистики: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

# Обробник помилок
@router.errors()
async def handle_errors(update: types.Update, exception: Exception):
    logger.error(f"Виникла помилка: {exception}")
    try:
        if update.message:
            await update.message.answer(
                loc.get_message("errors.general"),
                reply_markup=MainMenu().get_main_menu()
            )
        elif update.callback_query:
            await update.callback_query.answer(
                loc.get_message("errors.general"),
                show_alert=True
            )
        else:
            logger.warning(f"Неочікуваний тип оновлення: {update}")
    except Exception as e:
        logger.error(f"Помилка при обробці помилки: {e}")
