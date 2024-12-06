# handlers/ai_handler.py

import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import settings
import openai

router = Router()
logger = logging.getLogger(__name__)

# Налаштування OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Функція для взаємодії з OpenAI
async def ask_openai(prompt: str, max_tokens: int = 500) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти є експертом Mobile Legends. Відповідай коротко і точно."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,  # Налаштування креативності
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        return "Не вдалося отримати відповідь. Спробуйте пізніше."

# Обробник команди /ai
@router.message(Command("ai"))
async def handle_openai_request(message: Message, state: FSMContext):
    user_prompt = message.text.partition(' ')[2].strip()  # Отримуємо текст після команди
    if not user_prompt:
        await message.answer("Введіть текст запиту після команди /ai.")
        return

    await message.answer("Запит обробляється, зачекайте...")
    response = await ask_openai(user_prompt)  # Виклик функції OpenAI
    await message.answer(response)
