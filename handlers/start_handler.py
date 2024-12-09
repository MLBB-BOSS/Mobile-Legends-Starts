Юfrom aiogram import Router, types
import logging

logger = logging.getLogger("start_handler")
router = Router()

@router.message(commands=["start"])
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} triggered /start command.")
    await message.answer("Привіт! Це Mobile Legends: Starts! 🚀 Оберіть команду для початку.")