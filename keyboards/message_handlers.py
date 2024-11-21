from aiogram import Router
from aiogram.types import CallbackQuery, Message
from keyboards.main_menu import MainMenu
from keyboards.builds_menu import BuildsMenuKeyboard

router = Router()

@router.message(commands=["start", "menu"])
async def send_main_menu(message: Message):
    await message.answer("Головне меню", reply_markup=MainMenu.get_keyboard())

@router.callback_query(lambda c: c.data == "menu_builds")
async def show_builds_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Розділ '⚜️ Білди'",
        reply_markup=BuildsMenuKeyboard.get_keyboard()
    )
