import logging

logger = logging.getLogger(__name__)

async def safe_edit_message_text(message, new_text, reply_markup=None):
    """
    Безпечно редагує повідомлення, уникаючи дублювання вмісту.
    Якщо новий текст і клавіатура не відрізняються від поточних, редагування не виконується.
    У разі помилки намагається надіслати нове повідомлення замість редагування.
    """
    try:
        # Перевірка на ідентичність вмісту
        if message.text == new_text and message.reply_markup == reply_markup:
            logger.info(f"Message {message.message_id} edit skipped: content and markup are identical.")
            return
        
        # Спроба редагування повідомлення
        await message.edit_text(new_text, reply_markup=reply_markup)
        logger.info(f"Message {message.message_id} edited successfully in chat {message.chat.id}.")
    
    except Exception as e:
        # Логування помилки редагування
        logger.error(f"Failed to edit message {message.message_id} in chat {message.chat.id}: {e}")
        
        try:
            # Альтернативний варіант – надіслати нове повідомлення
            await message.answer(new_text, reply_markup=reply_markup)
            logger.info(f"Sent fallback message in chat {message.chat.id} for message {message.message_id}.")
        except Exception as fallback_error:
            # Логування помилки під час fallback
            logger.error(f"Failed to send fallback message in chat {message.chat.id}: {fallback_error}")
