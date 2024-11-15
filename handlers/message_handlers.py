# handlers/messages.py
from aiogram import F

@router.message(F.text)
async def handle_message(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Будь ласка, спочатку зареєструйтесь використовуючи /start")
        return
        
    # Тут логіка обробки повідомлень
    await message.answer("Я отримав ваше повідомлення!")
