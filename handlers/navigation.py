# handlers/navigation.py

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging

from states.states import MenuStates
from utils.constants import NAVIGATION_MENU_TEXT, NAVIGATION_INTERACTIVE_TEXT
from utils.keyboards import get_navigation_menu, get_generic_inline_keyboard, get_main_keyboard
from utils.message_utils import safe_delete_message

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    # Видалення повідомлення користувача
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    # Отримання даних стану
    data = await state.get_data()
    old_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    
    # Видалення старого "пульта"
    if old_message_id:
        await safe_delete_message(bot, message.chat.id, old_message_id)
    
    # Відправка нового "пульта"
    new_message = await bot.send_message(
        chat_id=message.chat.id,
        text=NAVIGATION_MENU_TEXT,
        reply_markup=get_navigation_menu()
    )
    
    # Оновлення або створення "екрану"
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=NAVIGATION_INTERACTIVE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        except TelegramBadRequest:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=NAVIGATION_INTERACTIVE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            interactive_message_id = interactive_message.message_id
    else:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=NAVIGATION_INTERACTIVE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        interactive_message_id = interactive_message.message_id
    
    # Збереження нового стану
    await state.update_data(
        bot_message_id=new_message.message_id,
        interactive_message_id=interactive_message_id,
        last_text=NAVIGATION_MENU_TEXT,
        last_keyboard=get_navigation_menu()
    )
    await state.set_state(MenuStates.NAVIGATION_MENU)

# Додайте інші хендлери для навігаційного меню тут
