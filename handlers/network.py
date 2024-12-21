# handlers/network.py

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from keyboards.main_keyboard import get_network_keyboard
from utils.graph_generator import create_network_graph
import logging

logger = logging.getLogger(__name__)

async def send_network_graph(message: types.Message):
    try:
        img_bytes = create_network_graph()
        await message.reply_photo(photo=img_bytes, caption="Взаємозв'язки Героїв у грі!", reply_markup=get_network_keyboard())
        logger.info("Граф взаємозв'язків надіслано користувачу %s", message.from_user.id)
    except Exception as e:
        logger.error("Помилка при генерації графіка: %s", e)
        await message.reply("Сталася помилка при генерації графіка. Спробуйте пізніше.")

async def refresh_graph(callback_query: types.CallbackQuery):
    try:
        img_bytes = create_network_graph()
        await callback_query.message.edit_media(media=types.InputMediaPhoto(media=img_bytes, caption="Взаємозв'язки Героїв у грі!"), reply_markup=get_network_keyboard())
        await callback_query.answer()
        logger.info("Граф взаємозв'язків оновлено для користувача %s", callback_query.from_user.id)
    except Exception as e:
        logger.error("Помилка при оновленні графіка: %s", e)
        await callback_query.answer("Сталася помилка при оновленні графіка.")

async def help_network(callback_query: types.CallbackQuery):
    help_text = "Це команда /network генерує граф взаємозв'язків героїв у грі Mobile Legends."
    await callback_query.message.answer(help_text)
    await callback_query.answer()
    logger.info("Допомога з командою /network надіслана користувачу %s", callback_query.from_user.id)

def register_network_handlers(dp: Dispatcher):
    dp.register_message_handler(send_network_graph, Command("network"))
    dp.register_callback_query_handler(refresh_graph, lambda c: c.data == "refresh_graph")
    dp.register_callback_query_handler(help_network, lambda c: c.data == "help_network")
