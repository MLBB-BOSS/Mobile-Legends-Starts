from aiogram import Router
from aiogram.types import Message
from services.ai_service import handle_gpt_query

menu_router = Router()

TRIGGER_WORDS = ["герой", "персонаж", "геймплей", "mlbb", "mobile legends"]

@menu_router.message()
async def handle_trigger_words(message: Message):
    """
    Обробляє повідомлення, що містять тригерні слова.
    """
    if any(trigger in message.text.lower() for trigger in TRIGGER_WORDS):
        prompt = f"Дай детальну інформацію про {message.text} у контексті Mobile Legends."
        response = await handle_gpt_query(prompt)
        await message.answer(response)
    else:
        await message.answer("Я поки що не розумію цього запиту. Спробуйте ще раз!")
