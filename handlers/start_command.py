from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from utils.localization_instance import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == '/start')
async def cmd_start(message: Message):
    logger.info(f"Користувач {message.from_user.id} запустив команду /start")
    try:
        await message.answer(
            loc.get_message("messages.start_command"),
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при виконанні команди /start: {e}")
        await message.answer(
            loc.get_message("errors.general")
        )
