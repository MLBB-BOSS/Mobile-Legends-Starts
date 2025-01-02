from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.menu_states import MainMenuState  # Імпортуємо стан
from keyboards.menus import get_navigation_menu

router = Router()

@router.message(MainMenuState.main)
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    # 1. Видалення повідомлення користувача
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # 2. Відправка нового повідомлення
    new_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🧭 Навігація:\n\nОберіть розділ для переходу.",
        reply_markup=get_navigation_menu()
    )

    # 3. Оновлення стану
    await state.update_data(bot_message_id=new_message.message_id)
    await state.set_state(MainMenuState.settings)  # Перехід на новий стан
