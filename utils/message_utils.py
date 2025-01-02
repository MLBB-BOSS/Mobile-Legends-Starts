# utils/message_utils.py

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int) -> bool:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        return True
    except TelegramBadRequest:
        return False
