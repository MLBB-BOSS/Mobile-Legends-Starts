async def cmd_start(self, message: Message, state: FSMContext):
    """Обробка команди /start"""
    # Видаляємо повідомлення користувача
    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    # Створюємо новий інтерактивний екран
    screen = await message.bot.send_message(
        chat_id=message.chat.id,
        text=MAIN_MENU_SCREEN_TEXT,
        reply_markup=get_main_menu_keyboard()
    )

    # Зберігаємо стан
    await state.set_state(MainMenuState.main)
    await state.update_data(
        bot_message_id=screen.message_id,
        last_text=MAIN_MENU_TEXT,
        last_keyboard=get_main_menu_keyboard()
    )
