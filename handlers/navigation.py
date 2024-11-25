# handlers/navigation.py
# UTC:22:00
# 2024-11-25
# Author: MLBB-BOSS
# Description: Navigation menu handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import get_navigation_keyboard
from keyboards.main_menu import get_main_keyboard
from keyboards.characters_menu import get_characters_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🛡️ Персонажі")
async def show_characters_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Персонажі'")
        await message.answer(
            "Оберіть тип героя:",
            reply_markup=get_characters_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in characters menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "📚 Гайди")
async def show_guides(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Гайди'")
        await message.answer(
            "📚 Розділ гайдів у розробці.\nТут будуть корисні поради та стратегії гри.",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in guides handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "⚖️ Контр-піки")
async def show_counterpicks(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Контр-піки'")
        await message.answer(
            "⚖️ Розділ контр-піків у розробці.\nТут ви зможете дізнатися про найкращі контр-піки проти кожного героя.",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in counterpicks handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "⚜️ Білди")
async def show_builds(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Білди'")
        await message.answer(
            "⚜️ Розділ білдів у розробці.\nТут будуть представлені найефективніші білди для кожного героя.",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in builds handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "📊 Голосування")
async def show_voting(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'Голосування'")
        await message.answer(
            "📊 Розділ голосування у розробці.\nТут ви зможете брати участь у різних опитуваннях.",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in voting handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text.in_({"🔙 Назад до Головного", "🔙 Назад"}))
async def return_to_main_menu(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to main menu")
        await message.answer(
            "Головне меню:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in return to main menu handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🔙 Назад до Навігації")
async def return_to_navigation(message: Message):
    try:
        logger.info(f"User {message.from_user.id} returned to navigation menu")
        await message.answer(
            "Меню навігації:",
            reply_markup=get_navigation_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in return to navigation handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")

# Обробники для типів героїв
@router.message(F.text.in_({"🗡️ Бійці", "🏹 Стрільці", "🔮 Маги", "🛡️ Танки", "🏥 Саппорти", "🗲 Гібриди"}))
async def show_heroes_by_type(message: Message):
    try:
        hero_type = message.text
        logger.info(f"User {message.from_user.id} selected hero type: {hero_type}")
        
        # Тут можна додати логіку вибору героїв за типом
        await message.answer(
            f"Розділ {hero_type} у розробці.\nТут буде список героїв цього типу.",
            reply_markup=get_characters_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in hero type handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
