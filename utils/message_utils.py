# utils/message_utils.py

import logging
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline_menus import get_generic_inline_keyboard
from texts import GENERIC_ERROR_MESSAGE_TEXT

logger = logging.getLogger(__name__)

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """Безпечне видалення повідомлення з обробкою виключень."""
    if message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Повідомлення {message_id} успішно видалено.")
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення {message_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard: InlineKeyboardMarkup = None,
    state: FSMContext = None,
    parse_mode: str = ParseMode.HTML
):
    """
    Перевірка зміни тексту або клавіатури перед редагуванням повідомлення.
    """
    if state:
        state_data = await state.get_data()
        last_text = state_data.get('last_text')
        last_keyboard = state_data.get('last_keyboard')

        if last_text == new_text and last_keyboard == new_keyboard:
            logger.info("Немає змін для редагування повідомлення.")
            return

    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
            reply_markup=new_keyboard,
            parse_mode=parse_mode
        )
        if state:
            await state.update_data(last_text=new_text, last_keyboard=new_keyboard)
        logger.info(f"Повідомлення {message_id} успішно оновлено.")
    except Exception as e:
        logger.error(f"Не вдалося редагувати повідомлення {message_id}: {e}")
        if state:
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )

async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    message_id: int = None,
    new_text: str = "",
    new_keyboard: InlineKeyboardMarkup = None,
    state: FSMContext = None,
    parse_mode: str = ParseMode.HTML
):
    """
    Відправляє нове інтерактивне повідомлення або редагує існуюче.
    
    :param bot: Екземпляр бота.
    :param chat_id: ID чату, куди відправляється повідомлення.
    :param message_id: ID повідомлення, яке потрібно редагувати. Якщо None, відправляється нове повідомлення.
    :param new_text: Новий текст повідомлення.
    :param new_keyboard: Нова клавіатура для повідомлення.
    :param state: Контекст стану FSM, якщо потрібна перевірка змін.
    :param parse_mode: Режим парсингу тексту.
    :return: ID відправленого або відредагованого повідомлення.
    """
    try:
        if message_id:
            # Якщо message_id заданий, спробуйте редагувати повідомлення
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=new_keyboard,
                parse_mode=parse_mode
            )
            logger.info(f"Повідомлення {message_id} успішно оновлено.")
            return message_id
        else:
            # Якщо message_id не заданий, відправте нове повідомлення
            message = await bot.send_message(
                chat_id=chat_id,
                text=new_text,
                reply_markup=new_keyboard,
                parse_mode=parse_mode
            )
            logger.info(f"Відправлено нове повідомлення {message.message_id} в чат {chat_id}.")
            return message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити або оновити інтерактивне повідомлення: {e}")
        if state:
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        return None