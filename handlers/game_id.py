from aiogram import Router, types
from aiogram.dispatcher.filters.command import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from states.profile_states import ProfileStates

game_id_router = Router()

@game_id_router.message(Command("set_game_id"))
async def set_game_id_handler(message: types.Message):
    await message.answer("📝 Введіть ваш ігровий ID Mobile Legends:")
    await ProfileStates.waiting_for_game_id.set()

@game_id_router.message(state=ProfileStates.waiting_for_game_id)
async def process_game_id(message: types.Message, state: FSMContext, db: AsyncSession):
    game_id = message.text.strip()

    if not game_id.isdigit():
        await message.answer("❌ Ігровий ID повинен складатися лише з цифр. Спробуйте ще раз.")
        return

    stmt = select(User).where(User.telegram_id == message.from_user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        await message.answer("❌ Ви ще не зареєстровані. Використовуйте команду /start.")
        return

    user.game_id = game_id
    await db.commit()

    await message.answer(f"✅ Ваш ігровий ID `{game_id}` успішно збережено.")
    await state.clear()
