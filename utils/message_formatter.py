import logging

logger = logging.getLogger(__name__)

async def safe_edit_message_text(message, new_text, reply_markup=None):
    """
    Безпечно редагує повідомлення, уникаючи дублювання вмісту.
    Якщо новий текст і клавіатура не відрізняються від поточних, редагування не виконується.
    """
    if message.text == new_text and message.reply_markup == reply_markup:
        logger.info("Message edit skipped: content and markup are identical.")
        return
    await message.edit_text(new_text, reply_markup=reply_markup)
