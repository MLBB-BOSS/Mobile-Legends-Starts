# handlers/navigation_handler.py

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import TelegramBadRequest, TelegramNetworkError
from keyboards.menus import get_inline_navigation_menu, MenuButton
import logging

logger = logging.getLogger(__name__)

dp = Dispatcher()

@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            "Ласкаво просимо до MoGonBot!",
            reply_markup=get_inline_navigation_menu()
        )
        logger.info(f"Користувач {message.from_user.id} викликав /start")
    except Exception as e:
        logger.error(f"Помилка при відправці /start: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@dp.callback_query_handler(lambda c: c.data == 'tournaments')
async def tournaments_menu(callback_query: types.CallbackQuery):
    try:
        await callback_query.answer()
        await callback_query.message.edit_text(
            "Оберіть дію з Турнірами:",
            reply_markup=get_tournaments_menu_inline()
        )
        logger.info(f"Користувач {callback_query.from_user.id} обрав Турніри")
    except TelegramBadRequest as e:
        logger.error(f"TelegramBadRequest при відображенні меню Турніри: {e}")
        await callback_query.message.answer("Не вдалося відобразити меню Турнірів.")
    except TelegramNetworkError as e:
        logger.error(f"TelegramNetworkError при відображенні меню Турніри: {e}")
        await callback_query.message.answer("Мережеві проблеми. Спробуйте пізніше.")
    except Exception as e:
        logger.error(f"Неочікувана помилка при відображенні меню Турніри: {e}")
        await callback_query.message.answer("Виникла помилка. Спробуйте ще раз.")
