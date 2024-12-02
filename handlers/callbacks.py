from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

router = Router()

@router.callback_query()
async def handle_callback(callback: CallbackQuery):
    if callback.data == "intro_next_1":
        await callback.message.edit_text(
            "Це друга сторінка вступу.",
            reply_markup=get_intro_page_2_keyboard()
        )
    elif callback.data == "intro_next_2":
        await callback.message.edit_text(
            "Це третя сторінка вступу.",
            reply_markup=get_intro_page_3_keyboard()
        )
    elif callback.data == "intro_start":
        await callback.message.edit_text("Вступ завершено. Розпочнемо!")
    elif callback.data == "mls_button":
        await callback.message.answer("Ви натиснули кнопку MLS!")
