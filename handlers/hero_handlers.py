# File: handlers/hero_handlers.py

from aiogram import Router, types, F
from utils.localization import loc
from keyboards.hero_menu import HeroMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

# Get all hero names from all classes
def _get_all_heroes():
    all_heroes = []
    try:
        classes = loc.get_message("heroes.classes")
        for class_info in classes.values():
            all_heroes.extend(class_info["heroes"])
        logger.debug(f"Loaded {len(all_heroes)} heroes")
        return all_heroes
    except Exception as e:
        logger.error(f"Error loading heroes list: {e}")
        return []

ALL_HEROES = _get_all_heroes()

@router.message(F.text.in_(ALL_HEROES))
async def handle_hero_selection(message: types.Message):
    """Handle hero selection and display hero information"""
    hero_name = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected hero: {hero_name}")

    try:
        # Get hero information
        hero_info = loc.get_message(f"heroes.info.{hero_name}")
        if not hero_info:
            raise KeyError(f"No information found for hero {hero_name}")

        # Create back button keyboard
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text=loc.get_message("buttons.back_to_hero_list"))],
                [types.KeyboardButton(text=loc.get_message("buttons.main_menu"))]
            ],
            resize_keyboard=True
        )

        # Send hero information
        await message.answer(
            text=hero_info,
            reply_markup=keyboard,
            parse_mode="HTML"  # Enable HTML formatting if your hero_info uses it
        )
        logger.debug(f"Successfully sent info about {hero_name} to user {user_id}")

    except KeyError as e:
        logger.warning(f"Hero information not found: {e}")
        await message.answer(
            text=loc.get_message("messages.errors.hero_not_found"),
            reply_markup=HeroMenu.get_keyboard()
        )
    except Exception as e:
        logger.exception(f"Error processing hero selection: {e}")
        await message.answer(
            text=loc.get_message("messages.errors.general"),
            reply_markup=HeroMenu.get_keyboard()
        )

# Back button handler
@router.message(F.text == loc.get_message("buttons.back_to_hero_list"))
async def back_to_hero_list(message: types.Message):
    """Handle back button to return to hero list"""
    try:
        keyboard = HeroMenu.get_keyboard()
        await message.answer(
            text=loc.get_message("messages.hero_menu"),
            reply_markup=keyboard
        )
        logger.info(f"User {message.from_user.id} returned to hero list")
    except Exception as e:
        logger.error(f"Error returning to hero list: {e}")
        await message.answer(loc.get_message("messages.errors.general"))
