# handlers/main_menu.py

import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from states import MenuStates
from keyboards.menus import get_main_menu, MenuButton
from texts import (
    MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION,
    MAIN_MENU_ERROR_TEXT, GENERIC_ERROR_MESSAGE_TEXT
)
from utils.shared_utils import (
    safe_delete_message, handle_error, transition_state, check_and_edit_message
)

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: types.Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробник двох кнопок: "Навігація", "Мій профіль" (та можливо BACK).
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} натиснув '{user_choice}' у головному меню")

    # Видаляємо повідомлення користувача
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if user_choice == MenuButton.NAVIGATION.value:
        # Перехід у стан NAVIGATION_MENU
        # Поки що просто відповімо текстом (або згенеруємо keyboard)
        # Щоб код не падав, можете або створити мінімальну keyboards та MenuStates, або заглушку
        await message.answer("Ви обрали 'Навігація' (функціонал ще в розробці).")
        # await transition_state(state, MenuStates.NAVIGATION_MENU)

    elif user_choice == MenuButton.PROFILE.value:
        # Перехід у стан PROFILE_MENU
        await message.answer("Ви обрали 'Мій Профіль' (функціонал ще в розробці).")
        # await transition_state(state, MenuStates.PROFILE_MENU)

    else:
        # Якщо хтось натиснув щось невідоме
        await message.answer("Невідома команда. Оберіть 'Навігація' або 'Мій Профіль'.")
