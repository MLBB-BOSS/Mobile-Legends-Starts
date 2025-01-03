# handlers/profile.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import F

from keyboards.menus import get_profile_menu
from texts import PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT, UNKNOWN_COMMAND_TEXT
from states import MenuStates
from utils.message_utils import safe_delete_message, check_and_edit_message, handle_error
from utils.db import get_user_profile
from utils.text_formatter import format_profile_text
from models.user import User
from models.user_stats import UserStats

router = Router()

@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile_handler(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик натискання кнопки "🪪 Мій Профіль".
    """
    await safe_delete_message(bot, message.chat.id, message.message_id)
    await process_my_profile(message, state, db, bot)

async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Функція для відображення профілю користувача.
    """
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)

    if profile_data:
        profile_info = {
            "username": profile_data.get('username', 'N/A'),
            "level": profile_data.get('level', 'N/A'),
            "rating": profile_data.get('rating', 'N/A'),
            "achievements_count": profile_data.get('achievements_count', 'N/A'),
            "screenshots_count": profile_data.get('screenshots_count', 'N/A'),
            "missions_count": profile_data.get('missions_count', 'N/A'),
            "quizzes_count": profile_data.get('quizzes_count', 'N/A'),
            "total_matches": profile_data.get('total_matches', 'N/A'),
            "total_wins": profile_data.get('total_wins', 'N/A'),
            "total_losses": profile_data.get('total_losses', 'N/A'),
            "tournament_participations": profile_data.get('tournament_participations', 'N/A'),
            "badges_count": profile_data.get('badges_count', 'N/A'),
            "last_update": profile_data.get('last_update').strftime('%d.%m.%Y %H:%M') if profile_data.get('last_update') else 'N/A'
        }
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Error formatting profile text: {e}")
            await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT)
            return

        # Генерація графіків для профілю
        try:
            overall_activity_bytes = create_overall_activity_graph()
            rating_bytes = create_rating_graph()
            game_stats_bytes = create_game_stats_graph()
        except Exception as e:
            logger.error(f"Помилка при генерації графіків профілю: {e}")
            overall_activity_bytes = rating_bytes = game_stats_bytes = None

        # Створення комбінованого зображення (опціонально)
        combined_image_bytes = None
        if overall_activity_bytes and rating_bytes and game_stats_bytes:
            try:
                # Відкриття зображень
                img1 = Image.open(io.BytesIO(overall_activity_bytes))
                img2 = Image.open(io.BytesIO(rating_bytes))
                img3 = Image.open(io.BytesIO(game_stats_bytes))

                # Встановлення розміру для графіків
                img1 = img1.resize((600, 400))
                img2 = img2.resize((600, 400))
                img3 = img3.resize((600, 400))

                # Створення нового зображення для об'єднання графіків
                combined_width = max(img1.width, img2.width, img3.width)
                combined_height = img1.height + img2.height + img3.height
                combined_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

                # Вставка графіків
                combined_image.paste(img1, (0, 0))
                combined_image.paste(img2, (0, img1.height))
                combined_image.paste(img3, (0, img1.height + img2.height))

                # Збереження комбінованого зображення в байтовий буфер
                buffer = io.BytesIO()
                combined_image.save(buffer, format="PNG")
                combined_image_bytes = buffer.getvalue()
            except Exception as e:
                logger.error(f"Помилка при об'єднанні графіків: {e}")

        # Форматування тексту профілю та надсилання графіків
        if combined_image_bytes:
            try:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=io.BytesIO(combined_image_bytes),
                    caption=formatted_profile_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_generic_inline_keyboard()
                )
                logger.info(f"Профіль користувача {user_id} надіслано з графіками.")
            except Exception as e:
                logger.error(f"Не вдалося надіслати графіки профілю: {e}")
                await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)
        else:
            try:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=formatted_profile_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_generic_inline_keyboard()
                )
                logger.info(f"Текстовий профіль користувача {user_id} надіслано.")
            except Exception as e:
                logger.error(f"Не вдалося надіслати текстовий профіль: {e}")
                await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

        # Надсилання нового звичайного повідомлення з текстом «🪪 Мій Профіль»
        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію для перегляду:",
                reply_markup=get_profile_menu()
            )
            await state.update_data(bot_message_id=my_profile_message.message_id)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення профілю: {e}")
            await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)
            return

        # Встановлення стану до PROFILE_MENU
        await state.set_state(MenuStates.PROFILE_MENU)
    ```

**Основні зміни:**

1. **Декоратори:** Переконайтеся, що всі декоратори використовують `@router.message()` або `@dp.message()` замість застарілих версій.

2. **Включення Роутера:** У вашому основному файлі `bot.py` переконайтеся, що ви включаєте роутери правильно.

## 6. Оновлення Основного Файлу `bot.py`

Переконайтеся, що ви включили всі роутери у вашому основному файлі `bot.py`. Ось приклад оновленого файлу:

```python
# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import logging

# Імпортуємо роутери
from handlers.base import router as base_router
from handlers.main_menu import router as main_menu_router
from handlers.profile import router as profile_router
# Імпортуйте інші роутери за потребою

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантажте змінні середовища з .env файлу
load_dotenv()

# Отримайте токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    exit(1)

# Створіть екземпляри бота та диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Включіть всі роутери до диспетчера
dp.include_router(base_router)
dp.include_router(main_menu_router)
dp.include_router(profile_router)
# Включіть інші роутери за потребою

async def main():
    try:
        # Запустіть диспетчер
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
