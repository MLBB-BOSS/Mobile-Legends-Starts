
from keyboards.menus import get_main_menu
from aiogram import Bot
from aiogram.fsm.context import FSMContext

async def load_main_menu(bot: Bot, state: FSMContext, chat_id: int, user_first_name: str):
    """
    Centralized function to load the main menu.
    """
    text = f"Вітаємо, {user_first_name}! Оберіть опцію:"
    keyboard = get_main_menu()
    message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    await state.update_data(bot_message_id=message.message_id)
