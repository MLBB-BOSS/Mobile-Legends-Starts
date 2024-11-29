# handlers/utils.py

import logging
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from keyboards.menus import get_main_menu
from keyboards.inline_menus import get_generic_inline_keyboard
from handlers.base import MenuStates  # Імпортуйте MenuStates з відповідного місця

logger = logging.getLogger(__name__)

async def handle_menu_transition(
    message_or_callback,
    state: FSMContext,
    bot: Bot,
    new_state,
    new_main_text: str,
    new_main_keyboard,
    new_interactive_text: str,
    remove_keyboard=False,
    additional_data: dict = None
):
    user_id = message_or_callback.from_user.id
    chat_id = message_or_callback.chat.id

    # Визначаємо, чи це повідомлення чи callback
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.delete()
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.answer()
    else:
        logger.error(f"Невідомий тип message_or_callback: {type(message_or_callback)}")
        return

    logger.info(f"Користувач {user_id} переходить до стану {new_state}")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=chat_id,
            text="Щось пішло не так. Почнімо спочатку.",
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Відправляємо нове повідомлення з клавіатурою
    try:
        if remove_keyboard:
            main_message = await bot.send_message(
                chat_id=chat_id,
                text=new_main_text,
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            main_message = await bot.send_message(
                chat_id=chat_id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
        new_bot_message_id = main_message.message_id

        # Видаляємо старе повідомлення
        await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Помилка при оновленні головного повідомлення: {e}")
        return

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        try:
            interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Помилка при відправці нового інтерактивного повідомлення: {e}")

    if additional_data:
        await state.update_data(**additional_data)

    await state.set_state(new_state)
