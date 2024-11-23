from aiogram import Router, F
from aiogram.types import Message
from keyboards.hero_menu import get_hero_class_menu  # Використовуємо функцію замість класу
from keyboards.main_menu import get_main_menu  # Використовуємо функцію замість класу
from utils.localization_instance import loc  # Імпортуємо локалізацію
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == loc.get_message("buttons.characters"))
async def show_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} запросив класи героїв")
    try:
        # Використовуємо функцію для отримання клавіатури
        keyboard = get_hero_class_menu()
        await message.answer(
            loc.get_message("messages.select_hero_class"),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Помилка при показі класів героїв: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=get_main_menu()
        )
