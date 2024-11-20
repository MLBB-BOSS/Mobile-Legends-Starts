# core/bot.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Обробник команди /start"""
    try:
        user_service = app_state.get_service('user_service')
        if user_service:
            await user_service.create_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username or "Anonymous"
            )
        
        # Create a keyboard
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Меню"))
        keyboard.add(KeyboardButton("Допомога"))

        await message.reply(
            "Вітаю! Я MLBB-BOSS бот для організації турнірів Mobile Legends. "
            "Використовуйте /help для перегляду доступних команд.",
            reply_markup=keyboard  # Add the keyboard here
        )
        app_state.increment_processed_commands()
        
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        await message.reply("Вибачте, сталася помилка. Спробуйте пізніше.")
