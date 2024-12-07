import os
import aiohttp  # Додано для роботи з HTTP-запитами
from aiogram import types, Dispatcher
from keyboards.menus import MenuButton
import logging

# Налаштування логування
logger = logging.getLogger("handlers_navigation")

# Отримання ключа OpenAI API з оточення
openai_api_key = os.getenv('OPENAI_API_KEY')
API_URL = "https://api.openai.com/v1/chat/completions"

# Функція для взаємодії з OpenAI через URL
async def ask_openai(prompt: str, max_tokens: int = 500) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        }
        json_data = {
            "model": "gpt-4",  # Використання моделі GPT-4
            "messages": [
                {"role": "system", "content": "Ти є експертом Mobile Legends. Відповідай коротко і точно."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=headers, json=json_data) as response:
                result = await response.json()
                return result['choices'][0]['message']['content'].strip()
    except aiohttp.ClientError as e:
        logger.error(f"HTTP error: {e}")
        return "Не вдалося отримати відповідь. Спробуйте пізніше."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Сталася непередбачувана помилка. Спробуйте пізніше."

async def show_meta_menu(message: types.Message):
    await message.answer("📈 <b>Мета:</b> Тут ви знайдете актуальну інформацію про мету гри.", parse_mode='HTML')

async def show_m6_menu(message: types.Message):
    await message.answer("🎮 <b>М6:</b> Останні новини та події про турніри M6.", parse_mode='HTML')

async def show_gpt_menu(message: types.Message):
    await message.answer("👾 Введіть ваше запитання для GPT:")

async def handle_gpt_query(message: types.Message):
    user_prompt = message.text
    if user_prompt:
        await message.answer("Запит обробляється, зачекайте...")
        response = await ask_openai(user_prompt)  # Виклик функції OpenAI
        await message.answer(response)

def register_navigation_handlers(dp: Dispatcher):
    dp.message.register(show_meta_menu, text=MenuButton.META.value)
    dp.message.register(show_m6_menu, text=MenuButton.M6.value)
    dp.message.register(show_gpt_menu, text=MenuButton.GPT.value)
    dp.message.register(handle_gpt_query)
