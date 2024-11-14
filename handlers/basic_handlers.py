from aiogram import F, Router, types

router = Router()

@router.message(F.text == "/start")
async def start_command(message: types.Message):
    """Команда /start."""
    await message.reply("Бот запущено!")
