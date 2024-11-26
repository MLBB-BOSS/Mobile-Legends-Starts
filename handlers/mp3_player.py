# handlers/mp3_player.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.mp3_player_menu import get_mp3_player_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🎵 MP3 Плеєр")
async def show_mp3_player(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'MP3 Плеєр'")
        await message.answer("Виберіть опцію MP3 плеєра:", reply_markup=get_mp3_player_keyboard())
    except Exception as e:
        logger.error(f"Error in MP3 player handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
