# handlers/message_handlers.py
from aiogram import Router, types, F
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message()
async def handle_unhandled_messages(message: types.Message):
    logger.info(
        loc.get_message("messages.unhandled_message", message=message.text)
    )
