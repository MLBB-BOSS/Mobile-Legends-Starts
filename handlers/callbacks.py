from aiogram.types import CallbackQuery
from aiogram import Router
from keyboards.inline_menus import intro_callback, generic_callback

router = Router()

@router.callback_query(intro_callback.filter())
async def handle_intro_callback(callback: CallbackQuery, callback_data: dict):
    page = callback_data["page"]
    if page == "2":
        await callback.message.edit_text(
            "Це друга сторінка вступу.",
            reply_markup=get_intro_page_2_keyboard()
        )
    elif page == "3":
        await callback.message.edit_text(
            "Це третя сторінка вступу.",
            reply_markup=get_intro_page_3_keyboard()
        )
    elif page == "start":
        await callback.message.edit_text("Вступ завершено. Розпочнемо!")

@router.callback_query(generic_callback.filter())
async def handle_generic_callback(callback: CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "mls_button":
        await callback.message.answer("Ви натиснули кнопку MLS!")
