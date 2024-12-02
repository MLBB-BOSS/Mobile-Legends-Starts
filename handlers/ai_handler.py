# handlers/ai_handler.py

import logging
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import OPENAI_API_KEY
from keyboards.inline_menus import get_generic_inline_keyboard
from utils.messages import (
    GENERIC_ERROR_MESSAGE_TEXT,
    AI_INTRO_TEXT,
    AI_RESPONSE_TEXT,
    UNKNOWN_COMMAND_TEXT,
)
from utils.hero_data import load_hero_data  # Імпорт функції для завантаження даних героя
from keyboards.menus import menu_button_to_class  # Імпорт відповідності кнопок класам

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізуємо OpenAI API
openai.api_key = OPENAI_API_KEY

# Створюємо Router для AI
router = Router()

# Визначаємо стани для AI
class AIStates(StatesGroup):
    WAITING_FOR_QUERY = State()

# Команда для початку взаємодії з AI
@router.message(F.text == "🧑‍💻 Допомога з персонажем")  # Використовуйте точний текст кнопки
async def ai_start(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} розпочав взаємодію з AI для персонажа")

    await message.delete()

    await state.set_state(AIStates.WAITING_FOR_QUERY)

    await bot.send_message(
        chat_id=message.chat.id,
        text=AI_INTRO_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )

# Обробник для отримання запиту від користувача
@router.message(AIStates.WAITING_FOR_QUERY)
async def ai_handle_query(message: Message, state: FSMContext, bot: Bot):
    user_query = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} запитує AI про персонажа: {user_query}")

    await message.delete()

    if not user_query:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть ім'я героя для отримання інформації.",
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Завантажуємо базову інформацію про героя
    hero_data = load_hero_data(user_query)
    if not hero_data:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Вибраний герой не знайдений. Будь ласка, перевірте назву героя або виберіть інший.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.clear()
        return

    # Формуємо промпт для OpenAI
    prompt = (
        f"Ось базова інформація про героя Mobile Legends:\n"
        f"Назва: {hero_data['name']} ({hero_data['name']})\n"
        f"Клас: {hero_data['class']}\n"
        f"Базові статистики:\n"
        f"  - Атака: {hero_data['base_statistics']['attack']}\n"
        f"  - Захист: {hero_data['base_statistics']['defense']}\n"
        f"  - Магія: {hero_data['base_statistics']['magic']}\n"
        f"  - Швидкість: {hero_data['base_statistics']['speed']}\n"
        f"Скіли:\n"
    )
    for skill_type, skill in hero_data['skills'].items():
        # У випадку наявності `energy_cost` чи інших додаткових полів
        skill_info = f"{skill['name']}: {skill['description']}"
        if "cooldown" in skill:
            skill_info += f" (Перезарядка: {skill['cooldown']})"
        if "mana_cost" in skill and skill['mana_cost'] is not None:
            skill_info += f" (Витрата мани: {skill['mana_cost']})"
        if "energy_cost" in skill and skill['energy_cost'] is not None:
            skill_info += f" (Витрата енергії: {skill['energy_cost']})"
        skill_info += "\n"
        prompt += f"  - {skill_info}"

    prompt += (
        "\n"
        "На основі цієї інформації, надайте детальний опис героя, його ролі у грі, рекомендації щодо використання скілів та загальні поради щодо гри за цього героя."
    )

    # Зберігаємо промпт в стані для можливого дебагу
    await state.update_data(last_prompt=prompt)

    # Викликаємо OpenAI API асинхронно
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant for Mobile Legends players."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        ai_reply = response.choices[0].message['content'].strip()

        # Відправляємо відповідь користувачу
        await bot.send_message(
            chat_id=message.chat.id,
            text=AI_RESPONSE_TEXT.format(response=ai_reply),
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )

        # Повертаємо користувача до головного меню
        await state.clear()

    except Exception as e:
        logger.error(f"Помилка при виклику OpenAI API: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.clear()

# Обробник для скасування взаємодії з AI
@router.message(F.text.lower() == "скасувати")
async def ai_cancel(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} скасував взаємодію з AI")

    await message.delete()
    await state.clear()

    await bot.send_message(
        chat_id=message.chat.id,
        text="Взаємодія з AI скасована.",
        reply_markup=get_generic_inline_keyboard()
    )
