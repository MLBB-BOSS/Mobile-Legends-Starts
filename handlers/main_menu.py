# handlers/main_menu.py
import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from states import MenuStates
from utils.shared_utils import safe_delete_message
from keyboards.menus import get_main_menu, MenuButton
from texts import MAIN_MENU_ERROR_TEXT

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    """
    Стан MAIN_MENU. Дві кнопки:
    - "Навігація"
    - "Мій Профіль"
    """
    user_choice = message.text
    logger.info(f"[MAIN_MENU] User {message.from_user.id} tapped: {user_choice}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if user_choice == MenuButton.NAVIGATION.value:
        # Переходимо до стану NAVIGATION_MENU
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer("Перехід до Навігації", reply_markup=None)
        # Потім у navigation/menu.py буде обробник @router.message(MenuStates.NAVIGATION_MENU)

    elif user_choice == MenuButton.PROFILE.value:
        # Переходимо до стану PROFILE_MENU
        await state.set_state(MenuStates.PROFILE_MENU)
        await message.answer("Перехід до Мого Профілю", reply_markup=None)
        # Потім у profile/menu.py буде обробник @router.message(MenuStates.PROFILE_MENU)

    else:
        # Невідома кнопка
        await message.answer(MAIN_MENU_ERROR_TEXT, reply_markup=get_main_menu())
