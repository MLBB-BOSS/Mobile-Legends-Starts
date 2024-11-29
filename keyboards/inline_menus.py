@router.callback_query(lambda c: c.data == "mls_button")
async def handle_mls_button(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    # Відповідаємо на callback, щоб уникнути зависання
    await callback_query.answer()

    # Виконуємо необхідну дію при натисканні кнопки
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Ви натиснули кнопку MLS!"
    )
