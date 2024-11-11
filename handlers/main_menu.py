# main.py

import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
import openai
from dotenv import load_dotenv
from typing import List

# Завантаження змінних оточення
load_dotenv()

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Налаштування OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Імпорт хендлерів та клавіатур
from handlers.start import start
from handlers.main_menu import (
    get_main_menu_keyboard,
    get_heroes_menu_keyboard,
    get_class_characters_keyboard
)
from data.characters import CHARACTERS
from data.classes import CLASSES

# Функція для відправки повідомлення
async def send_reply(update: Update, text: str, reply_markup=None) -> None:
    try:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Помилка при відправці повідомлення: {e}")

# Отримання персонажів за класом
def get_characters_by_class(character_class: str) -> List[str]:
    return CHARACTERS.get(character_class, [])

# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    user_id = update.effective_user.id
    logger.info(f"Отримано повідомлення від {user_id}: {user_input}")

    # Можна видалити перевірку мови, якщо всі повідомлення українською
    try:
        lang = detect(user_input)
        logger.info(f"Визначена мова повідомлення: {lang}")
    except Exception as e:
        logger.error(f"Помилка визначення мови: {e}")
        await send_reply(update, "Не вдалося визначити мову повідомлення.")
        return

    # Обробка вибору з меню
    if user_input in ["📰 Новини", "📚 Гайди", "🔧 Оновлення", "📘 Поради для новачків", "🏆 Турніри", "🦸 Герої", "❓ Допомога"]:
        await handle_menu_selection(update, user_input)
    elif user_input in CLASSES:
        await handle_hero_class_selection(update, context, user_input)
    elif user_input in get_characters_by_class(context.user_data.get('hero_class', '')):
        context.user_data['character'] = user_input
        await send_final_request(update, context)
    elif user_input == "Назад":
        await handle_back(update, context)
    else:
        await handle_gpt_query(update, user_input)

# Обробка вибору з головного меню
async def handle_menu_selection(update: Update, user_input: str) -> None:
    if user_input == "🦸 Герої":
        reply_markup = get_heroes_menu_keyboard()
        await send_reply(update, "Оберіть клас героя:", reply_markup=reply_markup)
    else:
        queries = {
            "📰 Новини": "Надайте останні новини про Mobile Legends на листопад 2024 року.",
            "📚 Гайди": "Які є корисні гайди для гри Mobile Legends на листопад 2024 року?",
            "🔧 Оновлення": "Які останні оновлення в Mobile Legends на листопад 2024 року?",
            "📘 Поради для новачків": "Які поради ви можете дати новачкам у Mobile Legends?",
            "🏆 Турніри": "Які найближчі турніри Mobile Legends?",
            "❓ Допомога": "Де я можу знайти допомогу по Mobile Legends?"
        }
        query = queries.get(user_input, "Невідома опція.")
        await handle_gpt_query(update, query)

# Обробка вибору класу героя
async def handle_hero_class_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, hero_class: str) -> None:
    context.user_data['hero_class'] = hero_class
    characters = get_characters_by_class(hero_class)
    if characters:
        reply_markup = get_class_characters_keyboard(hero_class)
        await send_reply(update, f"Оберіть героя класу {hero_class}:", reply_markup=reply_markup)
    else:
        await send_reply(update, f"Для класу {hero_class} немає доступних героїв.")

# Обробка кнопки "Назад"
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробник кнопки 'Назад'
    """
    if 'character' in context.user_data:
        # Повернення до вибору героя
        hero_class = context.user_data.get('hero_class')
        if hero_class:
            reply_markup = get_class_characters_keyboard(hero_class)
            await send_reply(update, f"Оберіть героя класу {hero_class}:", reply_markup=reply_markup)
        else:
            await send_reply(update, "Оберіть опцію з меню:", reply_markup=get_main_menu_keyboard())
    elif 'hero_class' in context.user_data:
        # Повернення до меню класів
        reply_markup = get_heroes_menu_keyboard()
        await send_reply(update, "Оберіть клас героя:", reply_markup=reply_markup)
    else:
        # Повернення до головного меню
        await start(update, context)

# Обробка запиту до GPT-4
async def handle_gpt_query(update: Update, user_input: str) -> None:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Виправлена назва моделі
            messages=[{"role": "user", "content": user_input}],
            max_tokens=1000,
            temperature=0.7
        )
        reply_text = response['choices'][0]['message']['content']
        formatted_reply = f"*Ваш запит:*\n{user_input}\n\n*Відповідь:*\n{reply_text}\n\n_Джерело: GPT-4_"
        await send_reply(update, formatted_reply)
    except openai.error.RateLimitError:
        logger.warning("Ліміт запитів досягнуто. Повтор спроби...")
        await send_reply(update, "Ліміт запитів перевищено. Спробуйте ще раз через декілька хвилин.")
    except openai.error.OpenAIError as e:
        logger.error(f"Помилка при запиті до GPT-4: {e}")
        await send_reply(update, "Сталась технічна помилка. Спробуйте ще раз.")
    except Exception as e:
        logger.error(f"Невідома помилка: {e}")
        await send_reply(update, "Невідома помилка. Спробуйте пізніше.")

# Надсилання запиту на інформацію про героя
async def send_final_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hero_class = context.user_data.get('hero_class')
    character = context.user_data.get('character')

    if hero_class and character:
        hero_info_request = (
            f"Надайте детальний опис та останню інформацію про героя {character} "
            f"з класу {hero_class} у грі Mobile Legends на листопад 2024 року."
        )
        logger.info(f"Запит на інформацію про героя {character} ({hero_class})")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": hero_info_request}],
                max_tokens=1000,
                temperature=0.7
            )
            reply_text = response['choices'][0]['message']['content']
            formatted_reply = f"*Інформація про героя {character}:*\n{reply_text}\n\n_Джерело: GPT-4_"
            await send_reply(update, formatted_reply)
        except openai.error.OpenAIError as e:
            logger.error(f"Помилка при запиті про героя: {e}")
            await send_reply(update, "Не вдалося отримати інформацію про героя. Ось загальний опис.")
            general_description_request = f"Надайте загальний опис героя {character}."
            await handle_gpt_query(update, general_description_request)
        except Exception as e:
            logger.error(f"Невідома помилка при запиті про героя: {e}")
            await send_reply(update, "Сталась помилка. Будь ласка, спробуйте знову.")

        # Очищення даних користувача після завершення
        context.user_data.clear()
    else:
        await send_reply(update, "Будь ласка, оберіть героя для отримання детальної інформації.")

# Налаштування Telegram-бота
def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.error("TELEGRAM_TOKEN не встановлено у змінних оточення.")
        return

    app = ApplicationBuilder().token(token).build()

    # Реєстрація хендлерів
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущений та готовий до роботи")
    app.run_polling()

if __name__ == "__main__":
    main()
