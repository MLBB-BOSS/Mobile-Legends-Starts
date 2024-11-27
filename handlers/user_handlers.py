from aiogram import Router, types
from aiogram.filters import Command
from models.user import User

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, db):
    try:
        # Перевіряємо чи користувач вже існує
        user = await db.get(User, {"telegram_id": message.from_user.id})
        
        if not user:
            # Створюємо нового користувача
            new_user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
            db.add(new_user)
            await db.commit()
            await message.answer(f"Вітаю! Ви успішно зареєстровані!")
        else:
            await message.answer(f"З поверненням, {user.username}!")
            
    except Exception as e:
        await message.answer("Виникла помилка при реєстрації. Спробуйте пізніше.")
        await db.rollback()
