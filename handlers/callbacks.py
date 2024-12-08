import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline_menus import get_generic_inline_keyboard, get_main_menu
from texts import (
    GENERIC_ERROR_MESSAGE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION
)
from handlers.base import MenuStates

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data.in_(["menu1", "menu2", "menu_back"]))
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено")
        await callback.answer(GENERIC_ERROR_MESSAGE_TEXT)
        return

    if data == "menu_back":
        # Повернення до головного меню
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info("Інтерактивне повідомлення успішно оновлено")
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)

        # Встановлюємо стан користувача на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await callback.answer("🔙 Ви повернулись до головного меню")
    elif data in ["menu1", "menu2"]:
        # Обробка інших меню
        if data == "menu1":
            await callback.answer("Ви обрали Меню 1")
            # Додайте логіку для Меню 1
        elif data == "menu2":
            await callback.answer("Ви обрали Меню 2")
            # Додайте логіку для Меню 2
    else:
        # Необроблені кнопки
        await callback.answer(UNHANDLED_INLINE_BUTTON_TEXT)
