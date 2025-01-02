from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
)

router = Router()


@router.callback_query(lambda callback: callback.data == "intro_next_1")
async def intro_page_2(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для другої сторінки інтро.
    """
    await callback.message.edit_text(
        text="🛠️ Цей бот допоможе вам:\n\n"
             "• 📊 Відстежувати свою статистику\n"
             "• 🏆 Організовувати турніри\n"
             "• 🥷 Дізнаватись про героїв",
        reply_markup=get_intro_page_2_keyboard(),
    )
    await state.set_state("intro_page_2")


@router.callback_query(lambda callback: callback.data == "intro_next_2")
async def intro_page_3(callback: CallbackQuery, state: FSMContext):
    """
    Обробник для третьої сторінки інтро.
    """
    await callback.message.edit_text(
        text="🎮 Готові почати гру? Натисніть «Розпочати», щоб перейти до головного меню.",
        reply_markup=get_intro_page_3_keyboard(),
    )
    await state.set_state("intro_page_3")


@router.callback_query(lambda callback: callback.data == "intro_start")
async def complete_intro(callback: CallbackQuery, state: FSMContext):
    """
    Завершення інтро.
    """
    await callback.message.edit_text(
        text="👋 Вітаємо в головному меню! Оберіть дію:",
        reply_markup=None,  # Замініть на головне меню, якщо воно реалізоване
    )
    await state.set_state("main_menu")
