# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from keyboards.hero_menu import HeroMenu  # Додано імпорт HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation_menu(message: Message):
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

@router.message(F.text == loc.get_message("buttons.guides"))
async def show_guides_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню гайдів")
    try:
        await message.answer(
            loc.get_message("messages.guides_menu"),
            reply_markup=NavigationMenu().get_guides_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню гайдів: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_heroes_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню персонажів")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_heroes_menu()  # Використовуємо HeroMenu замість NavigationMenu
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню персонажів: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.counter_picks"))
async def show_counter_picks_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню контр-піків")
    try:
        await message.answer(
            loc.get_message("messages.counter_picks_menu"),
            reply_markup=NavigationMenu().get_counter_picks_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню контр-піків: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.builds"))
async def show_builds_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню збірок")
    try:
        await message.answer(
            loc.get_message("messages.builds_menu"),
            reply_markup=NavigationMenu().get_builds_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню збірок: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.voting"))
async def show_voting_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню голосування")
    try:
        await message.answer(
            loc.get_message("messages.voting_menu"),
            reply_markup=NavigationMenu().get_voting_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню голосування: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.statistics"))
async def show_statistics(message: Message):
    logger.info(f"Користувач {message.from_user.id} запросив статистику")
    stats = {
        "games": 0,
        "wins": 0,
        "winrate": 0
    }
    try:
        games_message = loc.get_message("messages.statistics_info.games").format(games=stats["games"])
        wins_message = loc.get_message("messages.statistics_info.wins").format(wins=stats["wins"])
        winrate_message = loc.get_message("messages.statistics_info.winrate").format(winrate=stats["winrate"])
        full_message = f"{games_message}\n{wins_message}\n{winrate_message}"
        
        await message.answer(
            full_message,
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні статистики: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.back"))
async def go_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    try:
        await message.answer(
            loc.get_message("messages.menu_welcome"),
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до головного меню: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.profile"))
async def show_profile_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив профільний кабінет")
    try:
        await message.answer(
            loc.get_message("messages.profile_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні профільного меню: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )
