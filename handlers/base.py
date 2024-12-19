# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery  # Залиште ці імпорти
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode  # Виправлений імпорт

from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from keyboards.menus import get_main_menu  # Імпорт нової клавіатури
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, GENERIC_ERROR_MESSAGE_TEXT
)

from handlers.menu_profile import setup_handlers as setup_profile_handlers  # Імпорт функції налаштування профільних обробників

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    PROFILE_MENU = State()
    # Додайте інші стани за потребою

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await message.delete()
    await state.set_state(MenuStates.INTRO_PAGE_1)
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)
        logger.info("Sent INTRO_PAGE_1_TEXT")
    except Exception as e:
        logger.error(f"Failed to send intro page 1: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Handling intro_next_1 for user {callback.from_user.id}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_2_keyboard()
        )
        logger.info("Successfully edited message to INTRO_PAGE_2_TEXT")
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer("Сталася помилка. Спробуйте ще раз.")
        return
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer("Переход до сторінки 2")

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Handling intro_next_2 for user {callback.from_user.id}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_3_keyboard()
        )
        logger.info("Successfully edited message to INTRO_PAGE_3_TEXT")
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer("Сталася помилка. Спробуйте ще раз.")
        return
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer("Переход до сторінки 3")

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Handling intro_start for user {callback.from_user.id}")
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагування існуючого інлайн повідомлення MLS до MAIN_MENU_DESCRIPTION
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
        logger.info("Successfully edited interactive message to MAIN_MENU_DESCRIPTION")
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        # Якщо редагування не вдалося, відправте нове інлайн повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
            logger.info("Sent MAIN_MENU_DESCRIPTION as new interactive message")
        except Exception as e2:
            logger.error(f"Failed to send MAIN_MENU_DESCRIPTION: {e2}")

    # Відправка звичайного повідомлення з меню за допомогою Reply Keyboard
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()  # Використання ReplyKeyboardMarkup
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
        logger.info("Sent MAIN_MENU_TEXT")
    except Exception as e:
        logger.error(f"Failed to send main menu: {e}")

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer("Вітаємо у головному меню!")

# Специфічні обробники для кнопок головного меню
@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Handling navigation for user {message.from_user.id}")
    # Ваш код для обробки навігації
    await message.answer("Ви обрали Навігацію. Тут буде ваш код.")

# Інтеграція профільного роутера
def setup_handlers(dp: Router):
    dp.include_router(profile_router)
