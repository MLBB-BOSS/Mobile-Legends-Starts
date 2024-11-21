from aiogram import Router, types
from aiogram.filters.text import Text  # Виправлений імпорт
from utils.localization import loc
from keyboards.hero_menu import HeroMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

# Припускаємо, що HERO_CLASSES вже визначений у вашому локалізаційному менеджері

@router.message(Text(equals=HERO_CLASSES.keys()))
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
    except Exception as e:
        logger.exception(f"Помилка при обробці вибору класу героїв: {e}")
        await message.answer(loc.get_message("messages.errors.general"))
