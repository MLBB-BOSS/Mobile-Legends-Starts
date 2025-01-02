# handlers/navigation.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.menu_states import MenuStates
from utils.keyboards import get_navigation_menu, get_main_keyboard

router = Router()

@router.message(F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext):
    await message.answer(
        "🧭 Навігаційне меню\n\n"
        "Оберіть розділ, який вас цікавить:",
        reply_markup=get_navigation_menu()
    )
    await state.set_state(MenuStates.NAVIGATION_MENU)

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu(message: Message, state: FSMContext):
    if message.text == "🔙 Головне меню":
        await message.answer(
            "Ви повернулися до головного меню",
            reply_markup=get_main_keyboard()
        )
        await state.set_state(MenuStates.MAIN_MENU)
