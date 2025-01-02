from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
    get_main_menu_keyboard,
)

router = Router()

@router.callback_query(lambda callback: callback.data == "intro_page_2")
async def intro_page_2(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для другої сторінки інтро.
    """
    await callback.message.edit_text(
        text="🛠️ Цей бот допоможе вам:\n\n"
             "• 📊 Відстежувати свою статистику\n"
             "• 🏆 Організовувати турніри\n"
             "• 🥷 Дізнаватись про героїв\n"
             "• 📚 Отримувати гайди та поради",
        reply_markup=get_intro_page_2_keyboard(),
    )
    await state.set_state("intro_page_2")


@router.callback_query(lambda callback: callback.data == "intro_page_3")
async def intro_page_3(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для третьої сторінки інтро.
    """
    await callback.message.edit_text(
        text="🎮 Готові почати гру?\n\n"
             "Натисніть «Розпочати», щоб перейти до головного меню.",
        reply_markup=get_intro_page_3_keyboard(),
    )
    await state.set_state("intro_page_3")


@router.callback_query(lambda callback: callback.data == "intro_finish")
async def complete_intro(callback: CallbackQuery, state: FSMContext):
    """
    Завершення інтро.
    """
    await callback.message.edit_text(
        text="👋 Вітаємо в головному меню!\n\n"
             "Оберіть дію нижче:",
        reply_markup=get_main_menu_keyboard(),
    )
    await state.set_state("main_menu")
    # Зберігаємо інформацію, що користувач завершив інтро
    await state.update_data(intro_completed=True)


@router.callback_query(lambda callback: callback.data == "intro_page_1")
async def intro_page_1(callback: CallbackQuery, state: FSMContext):
    """
    Повернення до першої сторінки інтро.
    """
    await callback.message.edit_text(
        text="👋 Вітаємо у боті!\n\n"
             "Давайте почнемо знайомство з основними функціями.",
        reply_markup=get_intro_page_1_keyboard(),
    )
    await state.set_state("intro_page_1")
