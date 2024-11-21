# handlers/message_handlers.py

from aiogram import Router, types
from aiogram.filters import Text  # Коректний імпорт
from utils.localization import loc
from keyboards.main_menu import MainMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Text(equals=loc.get_message("buttons.navigation")))
async def navigation_handler(message: types.Message):
    try:
        await message.answer(
            "Ви обрали Навігацію.",
            reply_markup=MainMenu().get_main_menu()
        )
        logger.info(f"Користувач {message.from_user.id} обрав Навігацію.")
    except Exception as e:
        logger.exception(f"Помилка в navigation_handler: {e}")
        await message.answer(
            loc.get_message("messages.errors.general")
        )

# Додайте інші хендлери за потреби
