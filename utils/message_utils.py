# utils/message_utils.py

from aiogram import Bot
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int) -> None:
    """
    Безпечне видалення повідомлення. Ігнорує помилки, якщо повідомлення вже видалено.

    :param bot: Екземпляр бота.
    :param chat_id: ID чату.
    :param message_id: ID повідомлення для видалення.
    """
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.debug(f"Повідомлення {message_id} видалено.")
    except Exception as e:
        logger.warning(f"Не вдалося видалити повідомлення {message_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard: InlineKeyboardMarkup,
    state: FSMContext,
    parse_mode: str = "HTML"
) -> None:
    """
    Перевіряє та редагує повідомлення, якщо текст або клавіатура змінилися.

    :param bot: Екземпляр бота.
    :param chat_id: ID чату.
    :param message_id: ID повідомлення для редагування.
    :param new_text: Новий текст повідомлення.
    :param new_keyboard: Нова клавіатура.
    :param state: Контекст FSM.
    :param parse_mode: Режим парсингу тексту.
    """
    # Реалізуйте логіку перевірки зміни тексту та клавіатури
    pass  # Використовується в основному файлі обробників