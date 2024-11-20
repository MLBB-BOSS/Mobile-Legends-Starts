# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.hero_menu import HeroMenu
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

@router.callback_query(lambda c: c.data.startswith('hero_class_'))
async def process_hero_class_selection(callback: CallbackQuery):
    class_key = callback.data.replace('hero_class_', '')
    logger.info(f"Користувач {callback.from_user.id} вибрав клас героя: {class_key}")
    try:
        class_name = loc.get_message(f"heroes.classes.{class_key}.name")
        await callback.message.edit_text(
            loc.get_message("messages.select_hero").format(class_name=class_name),
            reply_markup=HeroMenu().get_heroes_by_class(class_key)
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні героїв класу {class_key}: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )

@router.callback_query(lambda c: c.data.startswith('hero_select_'))
async def process_hero_selection(callback: CallbackQuery):
    hero_id = callback.data.replace('hero_select_', '')
    logger.info(f"Користувач {callback.from_user.id} вибрав героя: {hero_id}")
    try:
        hero_info = loc.get_message(f"heroes.info.{hero_id}")
        if not hero_info:
            raise KeyError(f"heroes.info.{hero_id}")
        await callback.message.edit_text(
            hero_info,
            reply_markup=HeroMenu().get_hero_details_menu(hero_id)
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні інформації про героя {hero_id}: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.hero_not_found"),
            reply_markup=HeroMenu().get_heroes_by_class(class_key)
        )

@router.callback_query(lambda c: c.data == 'back_to_hero_classes')
async def back_to_hero_classes(callback: CallbackQuery):
    logger.info(f"Користувач {callback.from_user.id} повертається до вибору класів героїв")
    try:
        await callback.message.edit_text(
            loc.get_message("messages.select_hero_class"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до меню класів героїв: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )

@router.callback_query(lambda c: c.data == 'back_to_hero_list')
async def back_to_hero_list(callback: CallbackQuery):
    logger.info(f"Користувач {callback.from_user.id} повертається до списку героїв")
    try:
        # Отримуємо class_key з повідомлення
        class_name_line = callback.message.text.split('\n')[0]
        class_name = class_name_line.replace(loc.get_message("messages.select_hero").split("{class_name}")[0], '').strip()
        # Знаходимо class_key за class_name
        hero_classes = loc.get_message("heroes.classes")
        class_key = None
        for key, value in hero_classes.items():
            if value["name"] == class_name:
                class_key = key
                break
        if not class_key:
            raise ValueError("Class key not found")
        await callback.message.edit_text(
            loc.get_message("messages.select_hero").format(class_name=class_name),
            reply_markup=HeroMenu().get_heroes_by_class(class_key)
        )
    except Exception as e:
        logger.exception(f"Помилка при поверненні до списку героїв: {e}")
        await callback.message.edit_text(
            loc.get_message("errors.general"),
            reply_markup=HeroMenu().get_hero_class_menu()
        )
