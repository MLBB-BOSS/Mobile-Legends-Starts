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

@router.message(MenuStates.MAIN_MENU, lambda message: message.text == "🧭 Навігація")
async def handle_navigation_transition(message: types.Message, state: FSMContext, bot: Bot):
    """Обробник переходу до навігаційного меню."""
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    # Встановлюємо стан навігаційного меню
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    # Відправляємо нове повідомлення з навігаційним меню
    await message.answer(
        text=NAVIGATION_MENU_TEXT,
        reply_markup=get_navigation_menu()
    )

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    """
    Обробник меню NAVIGATION_MENU.
    Обробляє всі кнопки навігаційного меню
    """
    user_choice = message.text
    logger.info(f"[NAVIGATION_MENU] User {message.from_user.id} tapped: {user_choice}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Маппінг кнопок до станів і повідомлень
    menu_options = {
        MenuButton.HEROES.value: (MenuStates.HEROES_MENU, "Ви перейшли до розділу героїв"),
        MenuButton.TOURNAMENTS.value: (MenuStates.TOURNAMENTS_MENU, "Ви перейшли до розділу турнірів"),
        MenuButton.GUIDES.value: (MenuStates.GUIDES_MENU, "Ви перейшли до розділу гайдів"),
        MenuButton.BUILDS.value: (MenuStates.BUILDS_MENU, "Ви перейшли до розділу білдів"),
        MenuButton.TEAMS.value: (MenuStates.TEAMS_MENU, "Ви перейшли до розділу команд"),
        MenuButton.CHALLENGE.value: (MenuStates.CHALLENGES_MENU, "Ви перейшли до розділу челенджів"),
        MenuButton.BUST.value: (MenuStates.BUST_MENU, "Ви перейшли до розділу бусту"),
        MenuButton.TRADING.value: (MenuStates.TRADING_MENU, "Ви перейшли до розділу торгівлі"),
        MenuButton.BACK.value: (MenuStates.MAIN_MENU, "Повернення до головного меню")
    }

    if user_choice in menu_options:
        new_state, response_text = menu_options[user_choice]
        await state.set_state(new_state)
        # Отримуємо відповідну клавіатуру для нового стану
        keyboard = get_navigation_menu()  # Тут можна додати логіку для різних клавіатур
        await message.answer(response_text, reply_markup=keyboard)
    else:
        await message.answer(
            "Функція в розробці або невідома команда",
            reply_markup=get_navigation_menu()
        )
