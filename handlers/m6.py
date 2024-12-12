# handlers/m6.py

from aiogram import Router, types, Dispatcher
from keyboards.menus import MenuButton, get_m6_menu
import logging

logger = logging.getLogger(__name__)

router = Router()

def register_handlers(dp: Dispatcher):
    # Обробник кнопки "🏆 M6"
    @dp.message_handler(lambda message: message.text == MenuButton.M6.value)
    async def m6_menu_handler(message: types.Message):
        await message.answer("Оберіть опцію M6:", reply_markup=get_m6_menu())

    # Обробник кнопки "🏆 Турнірна Інформація"
    @dp.message_handler(lambda message: message.text == MenuButton.M6_INFO.value)
    async def m6_info_handler(message: types.Message):
        # Заглушка для відображення інформації про M6
        m6_info = "Турнірна Інформація: ... (замініть на реальні дані)"
        await message.answer(m6_info, reply_markup=get_m6_menu())

    # Обробник кнопки "📈 Статистика M6"
    @dp.message_handler(lambda message: message.text == MenuButton.M6_STATS.value)
    async def m6_stats_handler(message: types.Message):
        # Заглушка для відображення статистики M6
        m6_stats = "Статистика M6: ... (замініть на реальні дані)"
        await message.answer(m6_stats, reply_markup=get_m6_menu())

    # Обробник кнопки "📰 Новини M6"
    @dp.message_handler(lambda message: message.text == MenuButton.M6_NEWS.value)
    async def m6_news_handler(message: types.Message):
        # Заглушка для відображення новин M6
        m6_news = "Новини M6: ... (замініть на реальні дані)"
        await message.answer(m6_news, reply_markup=get_m6_menu())