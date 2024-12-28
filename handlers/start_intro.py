# handlers/start_intro.py

import logging
from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from states import MenuStates
from keyboards.menus import get_main_menu  # ваша функція, що повертає клавіатуру гол.меню
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
    get_generic_inline_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT,
    MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION, GENERIC_ERROR_MESSAGE_TEXT
)
from utils.shared_utils import (
    handle_error, transition_state, check_and_edit_message, 
    send_or_update_interactive_message, safe_delete_message
)
import models.user
import models.user_stats

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробник /start. Реєстрація користувача + показ інтро.
    """
    user_id = message.from_user.id
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реєстрація користувача (спрощена логіка)
    try:
        async with db.begin():
            user_result = await db.execute(
                select(models.user.User).where(models.user.User.telegram_id == user_id)
            )
            user = user_result.scalars().first()

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
                logger.info(f"Зареєстровано нового користувача: {user_id}")
            else:
                logger.info(f"Існуючий користувач: {user_id}")
    except Exception as e:
        logger.error(f"Помилка при реєстрації користувача {user_id}: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())
        return

    # Переходимо у стан INTRO_PAGE_1
    await transition_state(state, MenuStates.INTRO_PAGE_1)
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.update_data(
            interactive_message_id=interactive_message.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard(),
            bot_message_id=None
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())

@router.callback_query()
async def handle_intro_callback(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробник колбеків з інтро:
    intro_next_1 -> INTRO_PAGE_2
    intro_next_2 -> INTRO_PAGE_3
    intro_start  -> MAIN_MENU
    """
    data = callback.data
    current_state = await state.get_state()
    user_id = callback.from_user.id
    logger.info(f"Користувач {user_id} натиснув '{data}' в інтро")

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
        await callback.answer("Перехід до наступної сторінки.")

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
        await callback.answer("Перехід до наступної сторінки.")

    elif data == "intro_start" and current_state == MenuStates.INTRO_PAGE_3.state:
        await transition_state(state, MenuStates.MAIN_MENU)

        user_first_name = callback.from_user.first_name or "Користувач"
        main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

        try:
            # Редагуємо інтро-повідомлення (щоб сховати кнопки інтро)
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )

            # Відправляємо нове звичайне повідомлення — головне меню
            main_menu_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=main_menu_text_formatted,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_menu_message.message_id)
            await callback.answer("Вітаємо! Ви перейшли до головного меню.")
        except Exception as e:
            logger.error(f"Не вдалося оновити інтро-повідомлення: {e}")
            await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, get_main_menu())

    else:
        logger.warning(f"Невідомий callback_data: {data}")
        await callback.answer("Вибачте, я не розумію цю команду.", show_alert=True)
