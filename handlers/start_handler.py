from aiogram import Router, types

router = Router()

@router.message(commands=["start"])
async def send_welcome(message: types.Message):
    """
    Обробник команди /start.
    Відповідає користувачу вітальним повідомленням.
    """
    await message.answer("Привіт! Я бот Mobile Legends: Starts! 🚀")
