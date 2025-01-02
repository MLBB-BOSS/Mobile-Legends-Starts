from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline_menus import get_intro_page_1_keyboard, get_intro_page_2_keyboard, get_intro_page_3_keyboard

router = Router()

@router.callback_query(lambda callback: callback.data == "intro_next_1")
async def intro_page_2(callback: CallbackQuery, state: FSMContext):
    """
    Перехід до сторінки 2 інтро.
    """
    await callback.message.edit_text(
        "🛠️ Цей бот допоможе вам:\n\n"
        "• 📊 Відстежувати свою статистику\n"
        "• 🏆 Організовувати турніри\n"
        "• 🥷 Знаходити інформацію про героїв",
        reply_markup=get_intro_page_2_keyboard()
    )
    await state.set_state(HeroStates.intro_page_2)

@router.callback_query(lambda callback: callback.data == "intro_next_2")
async def intro_page_3(callback: CallbackQuery, state: FSMContext):
    """
    Перехід до сторінки 3 інтро.
    """
    await callback.message.edit_text(
        "🎮 Готові розпочати? Натисніть «Розпочати», щоб перейти до головного меню.",
        reply_markup=get_intro_page_3_keyboard()
    )
    await state.set_state(HeroStates.intro_page_3)

@router.callback_query(lambda callback: callback.data == "intro_start")
async def complete_intro(callback: CallbackQuery, state: FSMContext):
    """
    Завершення інтро.
    """
    await state.update_data(intro_completed=True)
    await callback.message.edit_text(
        "👋 Вітаю в головному меню! Оберіть дію:",
        reply_markup=get_main_menu_keyboard()
    )
    await state.set_state(HeroStates.main)
