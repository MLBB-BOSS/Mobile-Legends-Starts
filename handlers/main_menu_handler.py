from aiogram import Router, types
from keyboards.menu_keyboards import get_main_menu
from keyboards.message_keyboards import get_message_menu

router = Router()

@router.message(commands=["start"])
async def start_menu(message: types.Message):
    """
    Основне меню.
    """
    await message.answer(
        "Вітаю в основному меню! Оберіть дію:",
        reply_markup=get_main_menu()
    )

@router.callback_query(text="manage_messages")
async def manage_messages(callback: types.CallbackQuery):
    """
    Відкриття меню керування повідомленнями.
    """
    await callback.message.edit_text(
        "Меню керування повідомленнями. Що бажаєте зробити?",
        reply_markup=get_message_menu()
    )
