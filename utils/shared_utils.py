# utils/shared_utils.py

import logging
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """Акуратно видаляє повідомлення, ігнорує помилки."""
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        pass

async def handle_error(bot: Bot, chat_id: int, error_message: str, logger: logging.Logger, reply_markup=None):
    """Надсилає повідомлення про помилку."""
    try:
        await bot.send_message(chat_id, error_message, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Помилка при відправці handle_error: {e}")

async def transition_state(state: FSMContext, new_state):
    """Перехід у новий стан без очищення даних."""
    await state.set_state(new_state)

async def check_and_edit_message(bot: Bot, chat_id: int, message_id: int, new_text: str, new_keyboard, state: FSMContext):
    """Редагує повідомлення, якщо текст чи клавіатура змінилися."""
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
            reply_markup=new_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося відредагувати повідомлення: {e}")
