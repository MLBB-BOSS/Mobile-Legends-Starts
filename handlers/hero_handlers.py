# handlers/hero_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Text
from keyboards.hero_menu import HeroMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()
hero_menu = HeroMenu()

@router.message(Text(text=loc.get_message("buttons.characters")))
async def show_hero_classes(message: Message):
    try:
        keyboard = hero_menu.get_hero_classes_menu()
        await message.answer(
            text=loc.get_message("messages.hero_menu.select_class"),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при показі класів героїв: {e}")
        await message.answer(text=loc.get_message("errors.general"))

@router.message(lambda message: any(
    message.text == loc.get_message(f"buttons.{class_name}") 
    for class_name in ["tanks", "fighters", "assassins", "mages", "marksmen", "supports"]
))
async def show_heroes_by_class(message: Message):
    try:
        # Визначаємо клас героя з повідомлення
        hero_class = next(
            class_name for class_name in ["tank", "fighter", "assassin", "mage", "marksman", "support"]
            if message.text == loc.get_message(f"buttons.{class_name}s")
        )
        
        keyboard = hero_menu.get_heroes_by_class(hero_class)
        await message.answer(
            text=loc.get_message("messages.hero_menu.select_hero").format(
                class_name=loc.get_message(f"heroes.classes.{hero_class}.name")
            ),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при показі героїв класу: {e}")
        await message.answer(text=loc.get_message("errors.general"))

@router.message(lambda message: any(
    message.text == hero 
    for hero_class in ["fighter", "tank", "assassin", "mage", "marksman", "support"]
    for hero in loc.get_message(f"heroes.classes.{hero_class}.heroes")
))
async def show_hero_info(message: Message):
    try:
        hero_info = loc.get_message(f"heroes.info.{message.text}")
        if hero_info:
            await message.answer(text=hero_info)
        else:
            await message.answer(text=loc.get_message("errors.hero_not_found"))
    except Exception as e:
        logger.error(f"Помилка при показі інформації про героя: {e}")
        await message.answer(text=loc.get_message("errors.general"))
