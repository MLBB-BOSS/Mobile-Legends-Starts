#handlers/game_id.py
@profile_router.message(Command("set_game_id"))
async def set_game_id_handler(message: types.Message):
    await message.answer("📝 Введіть ваш ігровий ID Mobile Legends:")
    await ProfileStates.waiting_for_game_id.set()

@profile_router.message(state=ProfileStates.waiting_for_game_id)
async def process_game_id(message: types.Message, state: FSMContext):
    game_id = message.text.strip()

    if not game_id.isdigit():
        await message.answer("❌ Ігровий ID повинен складатися лише з цифр. Спробуйте ще раз.")
        return

    db: Session = next(get_db())
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user:
        await message.answer("❌ Ви ще не зареєстровані. Використовуйте команду /start.")
        return

    user.game_id = game_id
    db.commit()

    await message.answer(f"✅ Ваш ігровий ID `{game_id}` успішно збережено.")
    await state.clear()
