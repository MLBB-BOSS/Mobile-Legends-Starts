# handlers/base.py

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_hero_class_menu,
    heroes_by_class,
)
from keyboards.inline_menus import (
    get_navigation_inline_menu,
    get_profile_inline_menu,
)

logger = logging.getLogger(__name__)
router = Router()

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    PROFILE_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"User {message.from_user.id} initiated /start")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"👋 Welcome, {user_name}, to the Mobile Legends Tournament Bot!\n\n"
        "🎮 This bot helps you:\n"
        "• Organize tournaments\n"
        "• Save hero screenshots\n"
        "• Track activity\n"
        "• Earn achievements\n\n"
        "Choose an option from the menu below 👇",
        reply_markup=get_main_menu(),
    )

@router.message(F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected Navigation")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "In the 'Navigation' section, you can find various options to view heroes, guides, builds, etc.",
        reply_markup=get_navigation_inline_menu()
    )

@router.callback_query(F.data == "go_navigation")
async def callback_go_navigation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await callback_query.message.answer(
        "Select a navigation option:",
        reply_markup=get_navigation_menu(),
    )

@router.callback_query(F.data == "more_navigation")
async def callback_more_navigation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(
        "In the 'Navigation' section, you can:\n"
        "- View heroes by class\n"
        "- Read guides\n"
        "- Create builds\n"
        "Choose 'Go to Navigation' to start.",
    )

@router.message(F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected My Profile")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "In the 'My Profile' section, you can view your activity, ranking, and game statistics.",
        reply_markup=get_profile_inline_menu()
    )

@router.callback_query(F.data == "go_profile")
async def callback_go_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(MenuStates.PROFILE_MENU)
    await callback_query.message.answer(
        "Select a profile option:",
        reply_markup=get_profile_menu(),
    )

@router.callback_query(F.data == "more_profile")
async def callback_more_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(
        "In the 'My Profile' section, you can:\n"
        "- View overall activity\n"
        "- Check your ranking\n"
        "- View game statistics",
    )

@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Unknown message from {message.from_user.id}: {message.text}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Sorry, I don't understand this command. Please use the menu below.",
        reply_markup=get_main_menu(),
    )

def setup_handlers(dp):
    dp.include_router(router)
