# handlers/start_intro.py

import logging
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

# Імпорт станів (нехай лежить у states.py з 1 по 99)
from states import MenuStates

# Імпортуємо ваші тексти та клавіатури
from texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT
from texts import MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION
from texts import GENERIC_ERROR_MESSAGE_TEXT, UNKNOWN_COMMAND_TEXT
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
    get_generic_inline_keyboard
)
from keyboards.menus import get_main_menu

# Допоміжні утиліти (припустимо, що вони вже існують у вас)
from utils.shared_utils import (
    safe_delete_message,
    handle_error,
    transition_state,
    check_and_edit_message
)

import models.user
import models.user_stats
from sqlalchemy.future import select

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """Обробник /start: реєстрація й перша сторінка інтро."""
    user_id = message.from_user.id
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реєстрація (спрощена)
    try:
        async with db.begin():
            result = await db.execute(
                select(models.user.User).where(models.user.User.telegram_id == user_id)
            )
            user = result.scalars().first()

            if not user:
                new_user = models.user.User(
                    telegram_id=user_id,
                    username=message.from_user.username
                )
                db.add(new_user)
                await db.flush()
                new_stats = models.user_stats.UserStats(user_id=new_user.id)
                db.add(new_stats)
                await db.commit()
                logger.info(f"Новий користувач: {user_id}")
            else:
                logger.info(f"Існуючий користувач: {user_id}")
    except Exception as e:
        logger.error(f"Помилка реєстрації користувача {user_id}: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())
        return

    # Переходимо в стан INTRO_PAGE_1
    await transition_state(state, MenuStates.INTRO_PAGE_1)
    try:
        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            reply_markup=get_intro_page_1_keyboard()
        )
        # Зберігаємо ID повідомлення
        await state.update_data(
            interactive_message_id=msg.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard(),
            bot_message_id=None
        )
    except Exception as e:
        logger.error(f"Не вдалося показати першу сторінку інтро: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())


@router.callback_query()
async def handle_intro_callback(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробка колбеків для трьох сторінок інтро:
    - intro_next_1 → INTRO_PAGE_2
    - intro_next_2 → INTRO_PAGE_3
    - intro_start  → MAIN_MENU
    """
    data = callback.data
    current_state = await state.get_state()
    user_id = callback.from_user.id

    if data == "intro_next_1" and current_state == MenuStates.INTRO_PAGE_1.state:
        await transition_state(state, MenuStates.INTRO_PAGE_2)
        await check_and_edit_message(
            bot=bot,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            new_text=INTRO_PAGE_2_TEXT,
            new_keyboard=get_intro_page_2_keyboard(),
            state=state
        )
        await callback.answer("Перехід на другу сторінку.")

    elif data == "intro_next_2" and current_state == MenuStates.INTRO_PAGE_2.state:
        await transition_state(state, MenuStates.INTRO_PAGE_3)
        await check_and_edit_message(
            bot=bot,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            new_text=INTRO_PAGE_3_TEXT,
            new_keyboard=get_intro_page_3_keyboard(),
            state=state
        )
        await callback.answer("Перехід на третю сторінку.")

    elif data == "intro_start" and current_state == MenuStates.INTRO_PAGE_3.state:
        # Завершуємо інтро, переходимо в MAIN_MENU
        await transition_state(state, MenuStates.MAIN_MENU)

        user_first_name = callback.from_user.first_name or "Користувач"
        main_menu_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

        try:
            # Редагуємо інтро-повідомлення, щоб сховати старі кнопки
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            # Надсилаємо окреме звичайне повідомлення зі звичайною клавіатурою
            main_menu_msg = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=main_menu_text,
                reply_markup=get_main_menu()
            )
            # Зберігаємо ID
            await state.update_data(bot_message_id=main_menu_msg.message_id)
            await callback.answer("Вітаємо! Ви перейшли до головного меню.")
        except Exception as e:
            logger.error(f"Не вдалося оновити інтро-повідомлення: {e}")
            await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())
    else:
        logger.warning(f"Невідомий колбек: {data}")
        await callback.answer("Невідома команда або інтро вже пройдено.", show_alert=True)
