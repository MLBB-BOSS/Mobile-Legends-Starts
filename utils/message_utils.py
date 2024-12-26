from typing import Optional

# Інші імпорти залишаються без змін

async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard: InlineKeyboardMarkup,
    message_id: Optional[int],  # Використовуємо Optional[int]
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
