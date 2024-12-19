import logging
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT,
    MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION, UNKNOWN_COMMAND_TEXT
)

# Логування
logger = logging.getLogger(__name__)

# Ініціалізація роутера
router = Router()

# Стан для меню
class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()

# Обробник команди /start
@router.message(F.text == "/start")
async def handle_start_command(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    logger.info(f"User {user_id} sent /start")

    # Відправка першої сторінки інтро
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)
        await state.set_state(MenuStates.INTRO_PAGE_1)
    except Exception as e:
        logger.error(f"Error sending intro page 1: {e}")

# Обробка кнопки "Далі" на першій сторінці
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get("interactive_message_id")

    # Перехід до другої сторінки
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_2_keyboard()
        )
        await state.set_state(MenuStates.INTRO_PAGE_2)
    except Exception as e:
        logger.error(f"Failed to edit to intro page 2: {e}")
    await callback.answer()

# Обробка кнопки "Далі" на другій сторінці
@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get("interactive_message_id")

    # Перехід до третьої сторінки
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_3_keyboard()
        )
        await state.set_state(MenuStates.INTRO_PAGE_3)
    except Exception as e:
        logger.error(f"Failed to edit to intro page 3: {e}")
    await callback.answer()

# Обробка кнопки "Розпочати" на третій сторінці
@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    # Показ головного меню
    try:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text,
            parse_mode=ParseMode.HTML
        )
        await state.set_state(MenuStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Error sending main menu: {e}")

    await callback.answer()

# Обробка невідомих команд
@router.message()
async def handle_unknown_command(message: Message, bot: Bot):
    logger.warning(f"Unknown command received: {message.text}")
    await bot.send_message(chat_id=message.chat.id, text=UNKNOWN_COMMAND_TEXT)
