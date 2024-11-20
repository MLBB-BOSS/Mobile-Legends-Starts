# handlers/message_handlers.py
from aiogram import Router, types, F
from utils.localization import loc
from keyboards.profile_menu import ProfileMenu  # Додаємо імпорт класу ProfileMenu
import logging

router = Router()
logger = logging.getLogger(__name__)
profile_menu = ProfileMenu()  # Створюємо екземпляр класу ProfileMenu

@router.message(F.text == loc.get_message("buttons.profile"))
async def cabinet_handler(message: types.Message):
    try:
        await message.answer(
            text=loc.get_message("messages.profile_menu"),
            reply_markup=profile_menu.get_profile_menu()
        )
    except Exception as e:
        logger.error(f"Помилка при обробці кнопки 'Мій Кабінет': {e}")
        await message.answer(loc.get_message("errors.general"))

@router.message()
async def handle_unhandled_messages(message: types.Message):
    logger.info(
        loc.get_message("messages.unhandled_message", message=message.text)
    )
