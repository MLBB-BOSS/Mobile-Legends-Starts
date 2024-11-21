# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from keyboards.hero_menu import HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

# ... Ваші попередні обробники ...

# Обробник вибору класу героя
@router.message(F.text.in_([
    loc.get_message("buttons.tanks"),
    loc.get_message("buttons.fighters"),
    loc.get_message("buttons.assassins"),
    loc.get_message("buttons.mages"),
    loc.get_message("buttons.marksmen"),
    loc.get_message("buttons.supports")
]))
async def select_hero_class(message: Message):
    hero_class_button = message.text
    hero_class = None

    # Знаходимо ключ класу героя за текстом кнопки
    for key in loc.get_message("heroes.classes").keys():
        if loc.get_message(f"buttons.{key}") == hero_class_button:
            hero_class = key
            break

    if hero_class is None:
        await message.answer(
            loc.get_message("errors.class_not_found"),
            reply_markup=HeroMenu().get_heroes_menu()
        )
        return

    logger.info(f"Користувач {message.from_user.id} обрав клас героїв: {hero_class}")

    await message.answer(
        loc.get_message("messages.hero_menu.select_hero").format(class_name=loc.get_message(f"heroes.classes.{hero_class}.name")),
        reply_markup=HeroMenu().get_heroes_by_class(hero_class)
    )

# Обробник вибору героя
@router.message(F.text.in_(
    [hero_name for hero_name in loc.get_all_hero_names()]
))
async def show_hero_info(message: Message):
    hero_name = message.text
    hero_info = loc.get_message(f"heroes.info.{hero_name}")

    if not hero_info:
        await message.answer(
            loc.get_message("errors.hero_not_found"),
            reply_markup=HeroMenu().get_heroes_menu()
        )
        return

    logger.info(f"Користувач {message.from_user.id} обрав героя: {hero_name}")

    await message.answer(
        hero_info,
        reply_markup=HeroMenu().get_hero_info_menu()
    )
