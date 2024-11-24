from aiogram import Router, F
from aiogram.types import Message

from keyboards import main_menu_keyboard
from utils import get_localized_text

router = Router()

def register_handlers_navigation(dp):
    dp.include_router(router)

@router.message(F.text == "Опція 1")
async def option_one(message: Message):
    await message.answer(get_localized_text("option_one_response"))

@router.message(F.text == "Опція 2")
async def option_two(message: Message):
    await message.answer(get_localized_text("option_two_response"))

@router.message(F.text == "Повернутися до головного меню")
async def back_to_main_menu(message: Message):
    await message.answer(
        get_localized_text("back_to_main_menu"),
        reply_markup=main_menu_keyboard()
    )

@router.message()
async def unknown_navigation(message: Message):
    await message.answer(get_localized_text("unknown_command"))
