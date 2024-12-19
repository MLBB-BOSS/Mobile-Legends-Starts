# handlers/menu_profile.py

import logging
from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram import Bot

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.db import get_user_profile  # Імпорт функції для отримання профілю
import models.user
import models.user_stats

from keyboards.menus import (
    MenuButton,
    get_profile_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu
)
from keyboards.inline_menus import get_generic_inline_keyboard
from texts import (
    PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    STATISTICS_MENU_TEXT, STATISTICS_INTERACTIVE_TEXT,
    ACHIEVEMENTS_MENU_TEXT, ACHIEVEMENTS_INTERACTIVE_TEXT,
    SETTINGS_MENU_TEXT, SETTINGS_INTERACTIVE_TEXT,
    FEEDBACK_MENU_TEXT, FEEDBACK_INTERACTIVE_TEXT,
    HELP_MENU_TEXT, HELP_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT
)

# Ініціалізація логування
logger = logging.getLogger(__name__)

# Ініціалізація роутера для профілю
menu_profile_router = Router()

# Визначення станів для профілю
class ProfileStates(StatesGroup):
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()

# Обробник кнопки "🪪 Мій Профіль"
@menu_profile_router.message(Text(equals="🪪 Мій Профіль", ignore_case=True))
async def handle_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    if profile_data:
        profile_message = (
            f"🔍 <b>Ваш Профіль:</b>\n\n"
            f"• 🏅 Ім'я користувача: {profile_data['username']}\n"
            f"• 🧬 Рівень: {profile_data['level']}\n"
            f"• 📈 Рейтинг: {profile_data['rating']}\n"
            f"• 🎯 Досягнення: {profile_data['achievements_count']} досягнень\n"
            f"• 📸 Скріншоти: {profile_data['screenshots_count']}\n"
            f"• 🎯 Місії: {profile_data['missions_count']}\n"
            f"• 🧩 Вікторини: {profile_data['quizzes_count']}\n"
            f"• 🏆 Загальні матчі: {profile_data['total_matches']}\n"
            f"• 🥇 Виграші: {profile_data['total_wins']}\n"
            f"• 🥈 Поразки: {profile_data['total_losses']}\n"
            f"• 🌟 Турнірні Участі: {profile_data['tournament_participations']}\n"
            f"• 🏅 Бейджів: {profile_data['badges_count']}\n"
            f"• 📅 Останнє оновлення: {profile_data['last_update'].strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Оберіть опцію, щоб редагувати свій профіль чи переглянути статистику."
        )

        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')  # ID попереднього звичайного повідомлення
        interactive_message_id = data.get('interactive_message_id')  # ID інлайн-повідомлення

        # Редагування існуючого інлайн-повідомлення з даними профілю
        if interactive_message_id:
            try:
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    text=profile_message,
                    parse_mode="HTML",
                    reply_markup=get_generic_inline_keyboard()  # Використовуйте відповідну інлайн клавіатуру
                )
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
                try:
                    interactive_message = await bot.send_message(
                        chat_id=message.chat.id,
                        text=profile_message,
                        parse_mode="HTML",
                        reply_markup=get_generic_inline_keyboard()
                    )
                    # Оновлення state з новим ID інлайн-повідомлення
                    await state.update_data(interactive_message_id=interactive_message.message_id)
                except Exception as e2:
                    logger.error(f"Не вдалося створити нове інтерактивне повідомлення: {e2}")
        else:
            # Якщо інлайн-повідомлення не існує, створіть нове
            try:
                interactive_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=profile_message,
                    parse_mode="HTML",
                    reply_markup=get_generic_inline_keyboard()
                )
                interactive_message_id = interactive_message.message_id
                await state.update_data(interactive_message_id=interactive_message_id)
            except Exception as e:
                logger.error(f"Не вдалося створити нове інтерактивне повідомлення: {e}")

        # Надсилання нового звичайного повідомлення з текстом «🪪 Мій Профіль»
        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію для перегляду:",
                reply_markup=get_profile_menu()  # Використовуйте відповідну звичайну клавіатуру
            )
            new_bot_message_id = my_profile_message.message_id
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення профілю: {e}")
            new_bot_message_id = None

        # Видалення старого звичайного повідомлення
        if old_bot_message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=old_bot_message_id)
            except Exception as e:
                logger.error(f"Не вдалося видалити старе повідомлення: {e}")

        # Оновлення стану з новими ідентифікаторами повідомлень
        if new_bot_message_id:
            await state.update_data(bot_message_id=new_bot_message_id)

        # Встановлення стану до PROFILE_MENU
        await state.set_state(ProfileStates.PROFILE_MENU)
    else:
        # Обробка випадку, коли дані профілю не знайдено
        error_message = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        try:
            await bot.send_message(chat_id=message.chat.id, text=error_message, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку: {e}")
        await state.set_state(ProfileStates.MAIN_MENU)

# Обробник кнопок у профільному меню
@menu_profile_router.message(ProfileStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(chat_id=message.chat.id, text=UNKNOWN_COMMAND_TEXT, reply_markup=get_main_menu())
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(ProfileStates.PROFILE_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про невідому команду: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = ProfileStates.PROFILE_MENU

    if user_choice == MenuButton.STATISTICS.value:
        new_main_text = STATISTICS_MENU_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = STATISTICS_INTERACTIVE_TEXT
        new_state = ProfileStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = ACHIEVEMENTS_MENU_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = ACHIEVEMENTS_INTERACTIVE_TEXT
        new_state = ProfileStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = SETTINGS_MENU_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = SETTINGS_INTERACTIVE_TEXT
        new_state = ProfileStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = FEEDBACK_MENU_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = FEEDBACK_INTERACTIVE_TEXT
        new_state = ProfileStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = HELP_MENU_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = HELP_INTERACTIVE_TEXT
        new_state = ProfileStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 Мій Профіль\nОберіть опцію для перегляду:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = ProfileStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = ProfileStates.PROFILE_MENU

    try:
        main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        return

    # Видалення старого звичайного повідомлення
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагування інлайн-повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e2:
            logger.error(f"Не вдалося створити нове інтерактивне повідомлення: {e2}")

    # Оновлення стану з новими ідентифікаторами повідомлень
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик зміни імені користувача
@menu_profile_router.message(ProfileStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    new_username = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is changing username to: {new_username}")
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    if new_username:
        try:
            # Оновлення імені користувача у базі даних
            result = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
            user = result.scalars().first()
            if user:
                user.username = new_username
                await db.commit()
                response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
                logger.info(f"User {user_id} changed username to: {new_username}")
            else:
                response_text = "❌ Користувача не знайдено. Зареєструйтесь, щоб змінити ім'я."
        except Exception as e:
            logger.error(f"Error updating username for user_id {user_id}: {e}")
            response_text = "❌ Виникла помилка при зміні імені користувача."
    else:
        response_text = "❌ Будь ласка, введіть нове ім'я користувача."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про зміну імені: {e}")

    await state.set_state(ProfileStates.SETTINGS_MENU)

# Обробчик отримання зворотного зв'язку
@menu_profile_router.message(ProfileStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} sent feedback: {feedback}")
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    if feedback:
        # Збереження зворотного зв'язку у базі даних або надсилання адміністратору
        # Наприклад, збереження у таблиці Feedback
        # from models.feedback import Feedback
        # new_feedback = Feedback(user_id=user_id, feedback=feedback)
        # db.add(new_feedback)
        # await db.commit()

        response_text = FEEDBACK_RECEIVED_TEXT
        logger.info(f"Feedback received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, надайте ваш зворотний зв'язок."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання зворотного зв'язку: {e}")

    await state.set_state(ProfileStates.FEEDBACK_MENU)

# Обробчик повідомлення про помилку
@menu_profile_router.message(ProfileStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} reported a bug: {bug_report}")
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    if bug_report:
        # Збереження звіту про помилку у базі даних або надсилання адміністратору
        # Наприклад, збереження у таблиці BugReports
        # from models.bug_report import BugReport
        # new_bug = BugReport(user_id=user_id, report=bug_report)
        # db.add(new_bug)
        # await db.commit()

        response_text = BUG_REPORT_RECEIVED_TEXT
        logger.info(f"Bug report received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання звіту про помилку: {e}")

    await state.set_state(ProfileStates.FEEDBACK_MENU)
