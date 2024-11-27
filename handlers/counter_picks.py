from aiogram import Router, F
from aiogram.types import Message
from keyboards.level3.counter_picks_menu import get_counter_picks_menu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "⚖️ Контр-піки")
async def counter_picks_menu_handler(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав '⚖️ Контр-піки'")
    await message.answer(
        "⚖️ Контр-піки: Оберіть опцію для продовження.",
        reply_markup=get_counter_picks_menu()
    )
