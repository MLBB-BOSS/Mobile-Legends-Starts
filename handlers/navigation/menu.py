# handlers/navigation/menu.py
import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from states import MenuStates
from utils.shared_utils import safe_delete_message
from keyboards.menus import get_navigation_menu, MenuButton
from texts import NAVIGATION_MENU_TEXT, NAVIGATION_INTERACTIVE_TEXT

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    """
    Обробник меню NAVIGATION_MENU.
    Кнопки: «Герої», «Білди», «Гайди», «Назад» тощо.
    """
    user_choice = message.text
    logger.info(f"[NAVIGATION_MENU] User {message.from_user.id} tapped: {user_choice}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if user_choice == MenuButton.HEROES.value:
        # Переходимо в стан HEROES_MENU, наприклад
        await state.set_state(MenuStates.HEROES_MENU)
        await message.answer("Ви обрали: Персонажі", reply_markup=get_navigation_menu())

    elif user_choice == MenuButton.BACK.value:
        # Повернення в MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer("Назад у головне меню")

    else:
        # Інші кнопки або невідомі
        await message.answer("Функція в розробці або невідома команда", reply_markup=get_navigation_menu())
