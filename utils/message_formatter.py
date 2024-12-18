import logging
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup

logger = logging.getLogger(__name__)

async def safe_edit_message_text(message: Message, new_text: str, reply_markup=None):
    """
    Безпечно редагує повідомлення для InlineKeyboardMarkup або відправляє нове зі звичайною клавіатурою.
    """
    try:
        # Редагування InlineKeyboardMarkup
        if isinstance(reply_markup, InlineKeyboardMarkup):
            if message.text == new_text and message.reply_markup == reply_markup:
                logger.info("Message edit skipped: content and markup are identical.")
                return

            await message.edit_text(new_text, reply_markup=reply_markup)
            logger.info(f"Message {message.message_id} edited successfully with InlineKeyboardMarkup.")
        else:
            # Обробка звичайного повідомлення з ReplyKeyboardMarkup
            logger.info("Processing new message with ReplyKeyboardMarkup.")
            
            # Відправка нового повідомлення
            new_message = await message.answer(new_text, reply_markup=reply_markup)
            logger.info(f"New message {new_message.message_id} sent successfully.")

            # Видалення попереднього повідомлення
            try:
                await message.delete()
                logger.info(f"Previous message {message.message_id} deleted successfully.")
            except Exception as e:
                logger.warning(f"Failed to delete previous message {message.message_id}: {e}")

    except Exception as e:
        logger.error(f"Error during message edit or resend: {e}")
        if isinstance(reply_markup, InlineKeyboardMarkup):
            await message.answer("Сталася помилка при оновленні меню.")
        else:
            await message.answer("Сталася помилка при відправленні нового повідомлення.")