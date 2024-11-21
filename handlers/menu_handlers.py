# File: handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from keyboards.navigation_menu import NavigationMenu
from keyboards.profile_menu import ProfileMenu
from utils.localization import loc
from typing import Dict
import logging

logger = logging.getLogger(__name__)

# Initialize router
router = Router()

# Initialize keyboards as class methods instead of instances
class MenuHandlers:
    @staticmethod
    def get_hero_class_map() -> Dict[str, str]:
        """Get mapping of localized class names to internal class identifiers"""
        return {
            loc.get_message("heroes.classes.tank.name"): "tank",
            loc.get_message("heroes.classes.fighter.name"): "fighter",
            loc.get_message("heroes.classes.assassin.name"): "assassin",
            loc.get_message("heroes.classes.mage.name"): "mage",
            loc.get_message("heroes.classes.marksman.name"): "marksman",
            loc.get_message("heroes.classes.support.name"): "support"
        }

# Navigation Menu Handlers
@router.message(F.text == loc.get_message("buttons.navigation"))
async def handle_navigation(message: Message):
    """Handle navigation menu button press"""
    try:
        await message.answer(
            text=loc.get_message("messages.navigation_menu") or "Оберіть розділ для навігації:",
            reply_markup=NavigationMenu.get_main_navigation()
        )
        logger.info(f"User {message.from_user.id} opened navigation menu")
    except Exception as e:
        logger.error(f"Error in navigation menu handler: {e}")
        await message.answer(loc.get_message("errors.general"))

# Character Selection Handlers
@router.message(F.text == loc.get_message("buttons.characters"))
async def handle_characters(message: Message):
    """Handle characters menu button press"""
    try:
        await message.answer(
            text=loc.get_message("messages.select_hero_class"),
            reply_markup=NavigationMenu.get_heroes_menu()
        )
        logger.info(f"User {message.from_user.id} opened heroes menu")
    except Exception as e:
        logger.error(f"Error in characters menu handler: {e}")
        await message.answer(loc.get_message("errors.general"))

# Hero Class Selection Handler
@router.message(F.text.in_(MenuHandlers.get_hero_class_map().keys()))
async def handle_hero_class(message: Message):
    """Handle hero class selection"""
    try:
        hero_class = MenuHandlers.get_hero_class_map().get(message.text)
        if not hero_class:
            raise ValueError(f"Unknown hero class: {message.text}")
        
        await message.answer(
            text=loc.get_message("messages.hero_menu.select_hero").format(
                class_name=message.text
            ),
            reply_markup=NavigationMenu.get_hero_class_menu(hero_class)
        )
        logger.info(f"User {message.from_user.id} opened {hero_class} class menu")
    except ValueError as ve:
        logger.warning(f"Invalid hero class selected: {ve}")
        await message.answer(loc.get_message("errors.class_not_found"))
    except Exception as e:
        logger.error(f"Error in hero class menu handler: {e}")
        await message.answer(loc.get_message("errors.general"))

# Back Navigation Handlers
@router.message(F.text == loc.get_message("buttons.back"))
async def handle_back_to_main(message: Message):
    """Handle back to main menu button press"""
    try:
        await message.answer(
            text=loc.get_message("messages.welcome"),
            reply_markup=MainMenu.get_keyboard()
        )
        logger.info(f"User {message.from_user.id} returned to main menu")
    except Exception as e:
        logger.error(f"Error in back to main menu handler: {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message(F.text == loc.get_message("buttons.back_to_navigation"))
async def handle_back_to_navigation(message: Message):
    """Handle back to navigation button press"""
    try:
        await message.answer(
            text=loc.get_message("messages.navigation_menu") or "Оберіть розділ для навігації:",
            reply_markup=NavigationMenu.get_main_navigation()
        )
        logger.info(f"User {message.from_user.id} returned to navigation menu")
    except Exception as e:
        logger.error(f"Error in back to navigation handler: {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message(F.text == loc.get_message("buttons.back_to_hero_classes"))
async def handle_back_to_hero_classes(message: Message):
    """Handle back to hero classes button press"""
    try:
        await message.answer(
            text=loc.get_message("messages.select_hero_class"),
            reply_markup=NavigationMenu.get_heroes_menu()
        )
        logger.info(f"User {message.from_user.id} returned to hero classes menu")
    except Exception as e:
        logger.error(f"Error in back to hero classes handler: {e}")
        await message.answer(loc.get_message("errors.general"))
