from aiogram import Router

router = Router()

# Ваші маршрути
@router.message(lambda message: message.text == "🧭 Навігація")
async def handle_navigation(message):
    await message.answer("Це навігація.")

@router.message(lambda message: message.text == "🪪 Профіль")
async def handle_profile(message):
    await message.answer("Це ваш профіль.")
