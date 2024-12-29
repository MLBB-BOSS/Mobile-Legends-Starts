# handlers/navigation/menu.py
import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from states import MenuStates
from utils.shared_utils import safe_delete_message
from keyboards.menus import (
    MenuButton, 
    get_navigation_menu,
    get_heroes_menu,
    get_builds_menu,
    get_guides_menu,
    get_tournaments_menu,
    get_teams_menu,
    get_challenges_menu,
    get_bust_menu,
    get_trading_menu,
    get_main_menu
)

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.MAIN_MENU, lambda message: message.text == MenuButton.NAVIGATION.value)
async def handle_navigation_transition(message: types.Message, state: FSMContext, bot: Bot):
    """Обробник переходу до навігаційного меню."""
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🧭 Навігаційне меню\n\nОберіть розділ, який вас цікавить:",
        reply_markup=get_navigation_menu()
    )

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
    """Обробник кнопок навігаційного меню."""
    user_choice = message.text
    logger.info(f"[NAVIGATION_MENU] User {message.from_user.id} tapped: {user_choice}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Словник відповідностей кнопок до станів та функцій створення клавіатур
    menu_options = {
        MenuButton.HEROES.value: (MenuStates.HEROES_MENU, get_heroes_menu, "Меню героїв"),
        MenuButton.BUILDS.value: (MenuStates.BUILDS_MENU, get_builds_menu, "Меню білдів"),
        MenuButton.GUIDES.value: (MenuStates.GUIDES_MENU, get_guides_menu, "Меню гайдів"),
        MenuButton.TOURNAMENTS.value: (MenuStates.TOURNAMENTS_MENU, get_tournaments_menu, "Меню турнірів"),
        MenuButton.TEAMS.value: (MenuStates.TEAMS_MENU, get_teams_menu, "Меню команд"),
        MenuButton.CHALLENGES.value: (MenuStates.CHALLENGES_MENU, get_challenges_menu, "Меню челенджів"),
        MenuButton.BUST.value: (MenuStates.BUST_MENU, get_bust_menu, "Меню бусту"),
        MenuButton.TRADING.value: (MenuStates.TRADING_MENU, get_trading_menu, "Меню торгівлі"),
        MenuButton.BACK.value: (MenuStates.MAIN_MENU, get_main_menu, "Головне меню")
    }

    if user_choice in menu_options:
        new_state, get_keyboard, text = menu_options[user_choice]
        await state.set_state(new_state)
        await message.answer(text, reply_markup=get_keyboard())
    else:
        logger.warning(f"Невідома опція меню: {user_choice}")
        await message.answer(
            "Невідома опція. Будь ласка, виберіть опцію з меню.",
            reply_markup=get_navigation_menu()
        )

# Додаткові обробники для кожного підменю можуть бути додані тут або в окремих файлах
