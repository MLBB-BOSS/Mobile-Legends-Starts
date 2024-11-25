# handlers/mp3_player.py
# UTC:23:39
# 2024-11-25
# Author: MLBB-BOSS
# Description: MP3 Player handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🎵 MP3 Плеєр")
async def show_mp3_player(message: Message):
    try:
        logger.info(f"User {message.from_user.id} selected 'MP3 Плеєр'")
        await message.answer(
            "MP3 Плеєр у розробці.\nТут буде функціонал для відтворення музики."
        )
    except Exception as e:
        logger.error(f"Error in MP3 player handler: {e}")
        await message.answer("Сталася помилка. Спробуйте пізніше.")
