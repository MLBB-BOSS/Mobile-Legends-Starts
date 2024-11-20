# handlers/message_handlers.py
from aiogram import Router, types, F
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

# Обробник для кнопки "Мій Кабінет"
@router.message(F.text == loc.get("buttons.profile"))  # використовуємо текст з JSON
async def cabinet_handler(message: types.Message):
    try:
        # Використовуємо локалізований текст для меню профілю
        await message.answer(
            text=loc.get("messages.profile_menu"),
            reply_markup=await create_profile_keyboard()  # створіть цю функцію в keyboards.py
        )
    except Exception as e:
        logger.error(f"Помилка при обробці кнопки 'Мій Кабінет': {e}")
        await message.answer(loc.get("errors.general"))

# Обробник для неопрацьованих повідомлень
@router.message()
async def handle_unhandled_messages(message: types.Message):
    logger.info(
        loc.get("messages.unhandled_message", message=message.text)
    )
