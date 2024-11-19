from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import MainMenu
from config.localization.localize import get_message as _
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Користувач {message.from_user.id} запустив бота")
    await message.answer(
        _("messages.start_command"),
        reply_markup=MainMenu().get_main_menu()
    )
