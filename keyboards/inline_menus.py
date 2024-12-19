if interactive_message_id:
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=new_inline_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        # Додатково зберігайте нове повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=new_text,
            reply_markup=new_inline_keyboard
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)