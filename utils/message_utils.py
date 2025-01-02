# utils/message_utils.py

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, MessageCantBeDeleted, MessageToDeleteNotFound
import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)


async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """
    Безпечне видалення повідомлення з обробкою винятків.
    """
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Повідомлення {message_id} успішно видалено в чаті {chat_id}.")
    except (MessageCantBeDeleted, MessageToDeleteNotFound) as e:
        logger.warning(f"Не вдалося видалити повідомлення {message_id} в чаті {chat_id}: {e}")
    except Exception as e:
        logger.error(f"Невідома помилка при видаленні повідомлення {message_id} в чаті {chat_id}: {e}")


async def check_and_edit_message(bot: Bot, chat_id: int, message_id: int, text: str, keyboard: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]):
    """
    Перевіряє можливість редагування повідомлення і редагує його.
    Повертає True, якщо редагування успішне, інакше False.
    """
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard
        )
        logger.info(f"Повідомлення {message_id} в чаті {chat_id} успішно відредаговано.")
        return True
    except TelegramBadRequest as e:
        logger.warning(f"Не вдалося відредагувати повідомлення {message_id} в чаті {chat_id}: {e}")
        return False
    except Exception as e:
        logger.error(f"Невідома помилка при редагуванні повідомлення {message_id} в чаті {chat_id}: {e}")
        return False