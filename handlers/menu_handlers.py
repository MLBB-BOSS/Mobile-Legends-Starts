from aiogram import Router, types, F  # Add F here
from utils.localization import loc
from keyboards.hero_menu import HeroMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

HERO_CLASSES = {
    "Танк": "tank",
    "Бійці": "fighter",
    "Асасини": "assassin",
    "Маги": "mage",
    "Стрільці": "marksman",
    "Підтримка": "support"
}

@router.message(F.text.in_(HERO_CLASSES.keys()))  # Updated filter syntax
async def handle_hero_class_selection(message: types.Message):
    logger.info(f"Користувач {message.from_user.id} вибрав клас героїв: {message.text}")
    try:
        class_key = HERO_CLASSES[message.text]
        heroes = loc.get_message(f"heroes.classes.{class_key}.heroes")
        keyboard = HeroMenu().get_heroes_by_class(class_key)
        
        await message.answer(
            loc.get_message("messages.hero_menu.select_hero").format(
                class_name=message.text
            ),
            reply_markup=keyboard
        )
    except KeyError:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(loc.get_message("messages.errors.class_not_found"))
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору класу героїв: {e}")
        await message.answer(loc.get_message("messages.errors.general"))
