# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.hero_menu import HeroMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню класів героїв")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню класів героїв: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.message(F.text == loc.get_message("buttons.navigation"))
async def show_navigation_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu().get_navigation_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text == loc.get_message("buttons.profile"))
async def show_profile_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню профілю")
    try:
        await message.answer(
            loc.get_message("messages.profile_menu"),
            reply_markup=ProfileMenu().get_profile_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню профілю: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu().get_main_menu()
        )

@router.message(F.text.in_([
    loc.get_message("buttons.tanks"),
    loc.get_message("buttons.fighters"),
    loc.get_message("buttons.assassins"),
    loc.get_message("buttons.mages"),
    loc.get_message("buttons.marksmen"),
    loc.get_message("buttons.supports")
]))
async def handle_hero_class_selection(message: Message):
    class_name = message.text
    logger.info(f"Користувач {message.from_user.id} вибрав клас героя: {class_name}")
    try:
        await message.answer(
            f"Ви вибрали клас {class_name}. Ця функція в розробці.",
            reply_markup=HeroMenu().get_hero_class_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору класу героя {class_name}: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
