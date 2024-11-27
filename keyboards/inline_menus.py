@router.message(MenuStates.SEARCH_HERO)
async def search_hero_handler(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} шукає героя {hero_name}")
    # Реалізуйте логіку пошуку героя
    await message.answer(f"Результати пошуку для героя '{hero_name}' ще не доступні.")
    # Повернутися до меню Персонажі
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "🔙 Повернення до меню Персонажі:",
        reply_markup=get_heroes_menu(),
    )
    # Відправляємо пусте повідомлення з інлайн-кнопками
    await message.answer(
        EMPTY_MESSAGE,
        reply_markup=get_generic_inline_keyboard()
    )
