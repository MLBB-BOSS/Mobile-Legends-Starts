from aiogram import Router, types
from aiogram.filters import Text
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Text(equals="menu"))
async def menu_handler(message: types.Message):
    try:
        await message.answer("Menu selected!")
    except Exception as e:
        logger.exception(f"Error in menu_handler: {e}")
        await message.answer("An error occurred.")
