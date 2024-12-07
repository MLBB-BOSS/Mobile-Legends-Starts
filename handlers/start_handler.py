# handlers/start_handler.py

import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.inline_menus import get_intro_page_1_keyboard, get_intro_page_2_keyboard, get_intro_page_3_keyboard
from texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION, GENERIC_ERROR_MESSAGE_TEXT
from handlers.base import MenuStates

logger = logging.getLogger(__name__)
router = Router()

class StartStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Встановлюємо стан користувача на INTRO_PAGE_1
    await state.set_state(StartStates.INTRO_PAGE_1)

    # Відправляємо перше інтерктивне повідомлення з кнопкою 'Далі'
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)

@router.callback_query(StartStates.INTRO_PAGE_1, F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(StartStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(StartStates.INTRO_PAGE_2, F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(StartStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(StartStates.INTRO_PAGE_3, F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    # Відправляємо основне меню з клавіатурою
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu()
    )

    # Оновлюємо ID основного повідомлення
    await state.update_data(bot_message_id=main_menu_message.message_id)

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Оновлюємо інтерактивне повідомлення з описом основного меню
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()
