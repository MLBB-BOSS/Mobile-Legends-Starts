from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
)
from keyboards.menus import get_main_menu  # Функція для звичайної клавіатури
from texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT

router = Router()

class StartStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()

@router.message(F.command == "start")
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    # Перша сторінка інтро
    await state.set_state(StartStates.INTRO_PAGE_1)
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )
    await state.update_data(interactive_message_id=interactive_message.message_id)
    await message.delete()

@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Друга сторінка інтро
    await state.set_state(StartStates.INTRO_PAGE_2)
    interactive_message_id = (await state.get_data()).get('interactive_message_id')
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_PAGE_2_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_2_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Третя сторінка інтро
    await state.set_state(StartStates.INTRO_PAGE_3)
    interactive_message_id = (await state.get_data()).get('interactive_message_id')
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_PAGE_3_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_3_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Головне меню після завершення інтро
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu()
    )
    await state.update_data(bot_message_id=main_menu_message.message_id)
    interactive_message_id = (await state.get_data()).get('interactive_message_id')
    if interactive_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=interactive_message_id)
    await state.set_state(StartStates.MAIN_MENU)
    await callback.answer()
