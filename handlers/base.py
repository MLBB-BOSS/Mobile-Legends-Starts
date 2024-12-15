from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from keyboards.menus import (
    get_main_menu, get_navigation_menu, get_generic_inline_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    UNKNOWN_COMMAND_TEXT
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = Router()


class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"User {message.from_user.id} invoked /start")
    await message.delete()
    await state.set_state(MenuStates.INTRO_PAGE_1)
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=get_generic_inline_keyboard()
    )
    await state.update_data(interactive_message_id=interactive_message.message_id)


@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await _update_message(
        callback, state, bot, INTRO_PAGE_2_TEXT, get_generic_inline_keyboard(), MenuStates.INTRO_PAGE_2
    )


@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await _update_message(
        callback, state, bot, INTRO_PAGE_3_TEXT, get_generic_inline_keyboard(), MenuStates.INTRO_PAGE_3
    )


@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    state_data = await state.get_data()
    interactive_message_id = state_data.get("interactive_message_id")

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text,
        reply_markup=get_main_menu()
    )
    await state.update_data(bot_message_id=main_menu_message.message_id)
    await state.set_state(MenuStates.MAIN_MENU)


@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in main menu")
    await message.delete()
    await _handle_menu_navigation(message, state, bot, user_choice, MenuStates.MAIN_MENU)


async def _handle_menu_navigation(
    message: Message, state: FSMContext, bot: Bot, user_choice: str, current_state
):
    data = await state.get_data()
    bot_message_id = data.get("bot_message_id")
    interactive_message_id = data.get("interactive_message_id")

    new_main_text, new_main_keyboard, new_state = _get_menu_details(user_choice)
    if not new_main_text:
        logger.warning("Unknown command")
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_state = current_state

    main_message = await bot.send_message(
        chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard
    )
    await state.update_data(bot_message_id=main_message.message_id)

    try:
        if bot_message_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete old message: {e}")

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text="Interactive Menu",
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Interactive Menu",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)


async def _update_message(
    callback: CallbackQuery, state: FSMContext, bot: Bot, text: str, keyboard, next_state
):
    state_data = await state.get_data()
    interactive_message_id = state_data.get("interactive_message_id")
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
        await state.set_state(next_state)
    except Exception as e:
        logger.error(f"Failed to edit message: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=keyboard
        )
    await callback.answer()


def _get_menu_details(user_choice):
    if user_choice == "Navigation":
        return "Navigation Menu", get_navigation_menu(), MenuStates.NAVIGATION_MENU
    # Add more menu options as needed
    return None, None, None


def setup_handlers(dp: Router):
    dp.include_router(router)