from aiogram import Router, types
from aiogram import F
from utils.localization import loc
from keyboards.hero_menu import HeroMenu
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Create router instance
router = Router()

# Define hero classes mapping
HERO_CLASSES = {
    "Танк": "tank",
    "Бійці": "fighter",
    "Асасини": "assassin",
    "Маги": "mage",
    "Стрільці": "marksman",
    "Підтримка": "support"
}

@router.message(F.text.in_(HERO_CLASSES.keys()))
async def handle_hero_class_selection(message: types.Message):
    """
    Handle user selection of a hero class.
    """
    logger.info(f"Користувач {message.from_user.id} вибрав клас героїв: {message.text}")
    try:
        # Get the key for the selected class
        class_key = HERO_CLASSES[message.text]

        # Retrieve heroes for the class from localization
        heroes = loc.get_message(f"heroes.classes.{class_key}.heroes")

        # Generate keyboard for the selected hero class
        keyboard = HeroMenu().get_heroes_by_class(class_key)
        
        # Send a message with the hero selection menu
        await message.answer(
            loc.get_message("messages.hero_menu.select_hero").format(
                class_name=message.text
            ),
            reply_markup=keyboard
        )
    except KeyError:
        # Handle cases where the class is not found
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(loc.get_message("messages.errors.class_not_found"))
    except Exception as e:
        # Log unexpected exceptions
        logger.exception(f"Помилка при обробці вибору класу героїв: {e}")
        await message.answer(loc.get_message("messages.errors.general"))
