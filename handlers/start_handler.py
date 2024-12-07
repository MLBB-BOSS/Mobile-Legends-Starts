# handlers/start_handler.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline_menus import get_intro_page_1_keyboard
from texts import INTRO_PAGE_1_TEXT
from handlers.base import MenuStates

logger = logging.getLogger(__name__)
router = Router()

class StartStates(StatesGroup):
    INTRO_PAGE_1 = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Встановлюємо стан користувача на INTRO_PAGE_1
    await state.set_state(StartStates.INTRO_PAGE_1)

    # Відправляємо перше інтерктивне повідомлення з кнопкою 'Далі'
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)
