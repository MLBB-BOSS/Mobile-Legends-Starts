from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from services.states import RegistrationStates  # Додано імпорт станів реєстрації

router = Router()

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Скасувати")]],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if user and user.is_registered:
        await message.answer(
            f"З поверненням, {user.nickname}! 👋",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await message.answer(
        "Ласкаво просимо! 🎮\nВведіть ваш нікнейм (мінімум 3 символи):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(RegistrationStates.waiting_for_nickname)

@router.message(F.text == "❌ Скасувати")
async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Реєстрацію скасовано. Щоб почати знову, введіть /start",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(RegistrationStates.waiting_for_nickname)
async def process_nickname(message: Message, state: FSMContext):
    nickname = message.text.strip()
    
    if len(nickname) < 3:
        await message.answer("Нікнейм закороткий. Спробуйте ще раз:")
        return
        
    await state.update_data(nickname=nickname)
    await message.answer(
        "Чудово! ✨\nТепер введіть ваш Game ID:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(RegistrationStates.waiting_for_game_id)

@router.message(RegistrationStates.waiting_for_game_id)
async def process_game_id(message: Message, state: FSMContext):
    game_id = message.text.strip()
    
    if not game_id.isdigit():
        await message.answer("Game ID має містити лише цифри. Спробуйте ще раз:")
        return
        
    user_data = await state.get_data()
    
    try:
        await register_user(
            telegram_id=message.from_user.id,
            nickname=user_data['nickname'],
            game_id=game_id
        )
        
        await message.answer(
            "✅ Реєстрацію завершено!\nТепер ви можете користуватись ботом.",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.answer(
            "❌ Помилка при реєстрації. Спробуйте пізніше.",
            reply_markup=ReplyKeyboardRemove()
        )
        
    await state.clear()
