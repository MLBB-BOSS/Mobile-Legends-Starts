# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Text
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.hero_menu import HeroMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

# Обробник для команди /start
@router.message(CommandStart())
async def start_command(message: Message):
    logger.info(f"Користувач {message.from_user.id} запустив бота")
    await message.answer(
        loc.get_message("messages.menu_welcome"),
        reply_markup=MainMenu.get_main_menu()
    )

# Обробник для кнопки "Навігація"
@router.message(Text(equals=loc.get_message("buttons.navigation")))
async def show_navigation_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu.get_main_navigation()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu.get_main_menu()
        )

# Обробник для кнопки "Мій Кабінет"
@router.message(Text(equals=loc.get_message("buttons.profile")))
async def show_profile_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню профілю")
    try:
        await message.answer(
            loc.get_message("messages.profile_menu"),
            reply_markup=ProfileMenu.get_profile_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню профілю: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu.get_main_menu()
        )

# Обробник для кнопки "Персонажі"
@router.message(Text(equals=loc.get_message("buttons.characters")))
async def show_heroes_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню персонажів")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu.get_hero_class_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню персонажів: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )

# Обробник для вибору класу героя
@router.message(Text(equals=[
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
        # Знаходимо ключ класу за назвою
        hero_classes = loc.get_message("heroes.classes")
        class_key = None
        for key, value in hero_classes.items():
            if value["name"] == class_name:
                class_key = key
                break
        if not class_key:
            raise ValueError("Class key not found")

        await message.answer(
            loc.get_message("messages.select_hero").format(class_name=class_name),
            reply_markup=HeroMenu.get_heroes_by_class(class_key)
        )
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору класу героя {class_name}: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu.get_hero_class_menu()
        )

# Обробник для вибору героя
@router.message(Text(in_=loc.get_all_hero_names()))
async def handle_hero_selection(message: Message):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} вибрав героя: {hero_name}")
    try:
        hero_info = loc.get_message(f"heroes.info.{hero_name}")
        if not hero_info:
            raise KeyError(f"heroes.info.{hero_name}")
        await message.answer(
            hero_info,
            reply_markup=HeroMenu.get_hero_details_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні інформації про героя {hero_name}: {e}")
        await message.answer(
            loc.get_message("errors.hero_not_found"),
            reply_markup=HeroMenu.get_hero_class_menu()
        )

# Обробник для кнопки "Гайди"
@router.message(Text(equals=loc.get_message("buttons.guides")))
async def show_guides_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню гайдів")
    try:
        await message.answer(
            loc.get_message("messages.guides_menu"),
            reply_markup=NavigationMenu.get_guides_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню гайдів: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )

# Обробник для кнопки "Контр-Піки"
@router.message(Text(equals=loc.get_message("buttons.counter_picks")))
async def show_counter_picks_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню контр-піків")
    try:
        await message.answer(
            "Меню контр-піків в розробці.",
            reply_markup=NavigationMenu.get_counter_picks_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню контр-піків: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )

# Обробник для кнопки "Збірки"
@router.message(Text(equals=loc.get_message("buttons.builds")))
async def show_builds_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню збірок")
    try:
        await message.answer(
            "Меню збірок в розробці.",
            reply_markup=NavigationMenu.get_builds_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню збірок: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )

# Обробник для кнопки "Голосування"
@router.message(Text(equals=loc.get_message("buttons.voting")))
async def show_voting_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню голосування")
    try:
        await message.answer(
            "Меню голосування в розробці.",
            reply_markup=NavigationMenu.get_voting_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню голосування: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )

# Обробник для кнопки "Назад" до головного меню
@router.message(Text(equals=loc.get_message("buttons.back")))
async def go_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    try:
        await message.answer(
            loc.get_message("messages.menu_welcome"),
            reply_markup=MainMenu.get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до головного меню: {e}")
        await message.answer(
            loc.get_message("errors.general")
        )

# Обробник для кнопки "⬅️ До навігації"
@router.message(Text(equals=loc.get_message("buttons.back_to_navigation")))
async def back_to_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню навігації")
    try:
        await message.answer(
            loc.get_message("messages.navigation_menu"),
            reply_markup=NavigationMenu.get_main_navigation()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до меню навігації: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=MainMenu.get_main_menu()
        )

# Обробник для кнопки "↩️ Назад до класів"
@router.message(Text(equals=loc.get_message("buttons.back_to_hero_classes")))
async def back_to_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню класів героїв")
    try:
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu.get_hero_class_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до меню класів героїв: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu.get_main_navigation()
        )
