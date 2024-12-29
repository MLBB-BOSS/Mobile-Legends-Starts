# handlers/profile/menu.py
import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from states import MenuStates
from keyboards.menus import get_profile_menu, MenuButton
from utils.shared_utils import safe_delete_message

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    """
    Обробник меню PROFILE_MENU.
    Кнопки: “Статистика”, “Досягнення”, “Налаштування”, “Назад” і т.д.
    """
    user_choice = message.text
    logger.info(f"[PROFILE_MENU] User {message.from_user.id} tapped: {user_choice}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if user_choice == MenuButton.STATISTICS.value:
        # Переходимо, наприклад, у стан STATISTICS_MENU (якщо існує)
        await state.set_state(MenuStates.STATISTICS_MENU)
        await message.answer("Ви обрали 'Статистика'", reply_markup=get_profile_menu())

    elif user_choice == MenuButton.BACK.value:
        # Повернення в MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer("Назад у головне меню")

    else:
        await message.answer("Функція в розробці або невідома команда", reply_markup=get_profile_menu())
