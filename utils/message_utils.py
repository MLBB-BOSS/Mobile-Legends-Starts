# utils/message_utils.py

import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Deleted message {message_id} in chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to delete message {message_id} in chat {chat_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard: InlineKeyboardMarkup,
    state: FSMContext,
    parse_mode: ParseMode = ParseMode.HTML
):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
            reply_markup=new_keyboard,
            parse_mode=parse_mode
        )
        logger.info(f"Edited message {message_id} in chat {chat_id}")
    except Exception as e:
        logger.error(f"Error editing message {message_id} in chat {chat_id}: {e}")
        raise

async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup,
    message_id: int | None,
    state: FSMContext,
    parse_mode: ParseMode = ParseMode.HTML
) -> int:
    try:
        if message_id:
            await check_and_edit_message(
                bot=bot,
                chat_id=chat_id,
                message_id=message_id,
                new_text=text,
                new_keyboard=keyboard,
                state=state,
                parse_mode=parse_mode
            )
            logger.info(f"Updated existing interactive message {message_id} in chat {chat_id}")
            return message_id
        else:
            message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
            logger.info(f"Sent new interactive message {message.message_id} in chat {chat_id}")
            return message.message_id
    except Exception as e:
        logger.error(f"Error sending or updating interactive message in chat {chat_id}: {e}")
        raise
