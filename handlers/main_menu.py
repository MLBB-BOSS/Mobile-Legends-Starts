from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import main_menu_keyboard
from utils.localization import get_localized_text

router = Router()

def register_handlers_main_menu(dp):
    dp.include_router(router)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        get_localized_text("greeting"),
        reply_markup=main_menu_keyboard()
    )

@router.message(text="Мій профіль")
async def my_profile(message: Message):
    await message.answer(get_localized_text("profile"))

@router.message(text="Навігація")
async def navigation(message: Message):
    from keyboards import navigation_menu_keyboard
    await message.answer(
        get_localized_text("navigation_prompt"),
        reply_markup=navigation_menu_keyboard()
    )

@router.message()
async def unknown_message(message: Message):
    await message.answer(get_localized_text("unknown_command"))
