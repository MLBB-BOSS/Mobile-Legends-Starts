from aiogram import Router, F
from aiogram.types import Message
from keyboards.level3.guides_menu import get_guides_menu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "📚 Гайди")
async def guides_menu_handler(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав '📚 Гайди'")
    await message.answer(
        "📚 Гайди: Оберіть потрібний розділ.",
        reply_markup=get_guides_menu()
    )
