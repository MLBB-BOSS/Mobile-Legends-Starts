# core/screenshot_handler.py

from aiogram import types
from core.bot import dp
from services.screenshot_service import handle_screenshot_upload

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    await handle_screenshot_upload(message)
