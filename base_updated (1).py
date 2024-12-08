
# Ensure necessary text constants exist
MAIN_MENU_TEXT = "Головне меню, {user_first_name}"
MAIN_MENU_DESCRIPTION = "Обери, куди хочеш перейти:"
PROFILE_MENU_TEXT = "Меню профілю. Обери опцію:"

# Define state transitions and button handling for each menu level
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    main_menu_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text,
        reply_markup=get_main_menu()
    )
    await state.update_data(bot_message_id=main_menu_message.message_id)
    interactive_message_id = (await state.get_data()).get('interactive_message_id')
    if interactive_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=interactive_message_id)
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()
