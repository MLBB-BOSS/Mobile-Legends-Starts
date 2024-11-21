# File: handlers/hero_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text.in_({
    loc.get_message("buttons.tanks"),
    loc.get_message("buttons.fighters"),
    loc.get_message("buttons.assassins"),
    loc.get_message("buttons.mages"),
    loc.get_message("buttons.marksmen"),
    loc.get_message("buttons.supports")
}))
async def handle_hero_class(message: Message):
    logger.info(f"Користувач {message.from_user.id} вибрав клас героїв: {message.text}")
    try:
        class_type = message.text
        # Get heroes for the selected class from your JSON data
        heroes = get_heroes_by_class(class_type)

        if heroes:
            # Create keyboard with heroes
            keyboard = create_heroes_keyboard(heroes)
            await message.answer(
                loc.get_message("messages.hero_menu.select_hero").format(
                    class_name=class_type
                ),
                reply_markup=keyboard
            )
        else:
            await message.answer(loc.get_message("errors.class_not_found"))
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору класу героїв: {e}")
        await message.answer(loc.get_message("errors.general"))

def get_heroes_by_class(class_type: str) -> list:
    # Map emoji to class names
    class_map = {
        "🛡 Танки": "tank",
        "⚔️ Бійці": "fighter",
        "🗡 Асасини": "assassin",
        "🔮 Маги": "mage",
        "🏹 Стрільці": "marksman",
        "✨ Підтримка": "support"
    }

    class_key = class_map.get(class_type)
    if class_key and class_key in loc.get_message("heroes.classes"):
        return loc.get_message(f"heroes.classes.{class_key}.heroes")
    return []

def create_heroes_keyboard(heroes: list) -> types.ReplyKeyboardMarkup:
    keyboard = []
    # Create rows with 2 heroes per row
    for i in range(0, len(heroes), 2):
        row = [
            types.KeyboardButton(text=heroes[i])
        ]
        if i + 1 < len(heroes):
            row.append(types.KeyboardButton(text=heroes[i + 1]))
        keyboard.append(row)

    # Add back button
    keyboard.append([
        types.KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes"))
    ])

    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
