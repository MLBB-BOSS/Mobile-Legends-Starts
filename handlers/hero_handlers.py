# File: handlers/hero_handlers.py

import logging
from aiogram import Router, F, types
from keyboards.navigation_keyboard import NavigationKeyboard
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🔍 Пошук Персонажа")
async def search_hero(message: types.Message):
    """Handle hero search"""
    try:
        await message.answer(
            text=loc.get_message("hero.search_prompt"),
            reply_markup=types.ForceReply()
        )
        logger.debug(f"Hero search initiated by user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in hero search: {e}")
        await message.answer(loc.get_message("error.general"))

@router.message(F.text.in_({"🛡️ Танк", "🔮 Маг", "🏹 Стрілець", "🗡️ Асасін", "🛠️ Підтримка"}))
async def show_hero_category(message: types.Message):
    """Handle hero category selection"""
    try:
        category = message.text.split()[1]  # Get category name without emoji
        await message.answer(
            text=loc.get_message(f"hero.category.{category.lower()}"),
            reply_markup=NavigationKeyboard().get_characters_menu()
        )
        logger.debug(f"Hero category {category} shown to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error showing hero category: {e}")
        await message.answer(loc.get_message("error.general"))
