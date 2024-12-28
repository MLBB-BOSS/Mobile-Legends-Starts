# handlers/main_menu.py

import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states import MenuStates
from keyboards.menus import get_main_menu, MenuButton
from utils.shared_utils import safe_delete_message

logger = logging.getLogger(__name__)
router = Router()

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: types.Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Головне меню: дві кнопки: "Навігація" і "Мій Профіль".
    Поки що робимо прості "заглушки".
    """
    user_choice = message.text
    await safe_delete_message(bot, message.chat.id, message.message_id)
    logger.info(f"Користувач {message.from_user.id} обрав: {user_choice}")

    if user_choice == MenuButton.NAVIGATION.value:
        await message.answer("Ви обрали 'Навігація'. (Функція в розробці)")
        # Можна було б переходити: await state.set_state(MenuStates.NAVIGATION_MENU)

    elif user_choice == MenuButton.PROFILE.value:
        await message.answer("Ви обрали 'Мій Профіль'. (Функція в розробці)")
        # await state.set_state(MenuStates.PROFILE_MENU)

    else:
        # Якщо хтось натиснув щось стороннє
        await message.answer("Невідома команда. Скористайтеся кнопками нижче:", reply_markup=get_main_menu())
