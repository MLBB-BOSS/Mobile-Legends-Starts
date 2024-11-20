from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import MainMenu
from utils.localization import loc  # Змінений імпорт
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Користувач {message.from_user.id} запустив бота")
    await message.answer(
        loc.get_message("messages.start_command"),
        reply_markup=MainMenu().get_main_menu()
    )
