# handlers/menu_profile.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode  # Виправлений імпорт

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from handlers.states import MenuStates  # Імпорт MenuStates
from keyboards.menus import (
    MenuButton, get_profile_menu, get_statistics_menu,
    get_achievements_menu, get_settings_menu, get_feedback_menu,
    get_help_menu, get_main_menu, get_generic_inline_keyboard
)
from texts import (
    MAIN_MENU_ERROR_TEXT, PROFILE_MENU_TEXT,
    UNKNOWN_COMMAND_TEXT, CHANGE_USERNAME_RESPONSE_TEXT, FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    MAIN_MENU_TEXT, MAIN_MENU_DESCRIPTION
)

from utils.db import get_user_profile  # При необхідності

# Ініціалізація логування
logger = logging.getLogger(__name__)

profile_router = Router()

# Обробник кнопки "🪪 Мій профіль"
@profile_router.message(F.text == "🪪 Мій профіль")
async def open_profile_menu(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    logger.info(f"User {message.from_user.id} clicked '🪪 Мій профіль'")
    user_id = message.from_user.id

    # Отримайте дані профілю користувача з бази даних
    profile_data = await get_user_profile(db=db, user_id=user_id)

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
        reply_markup = get_profile_menu()
    else:
        profile_message = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        reply_markup = get_generic_inline_keyboard()

    # Відправка профільного повідомлення
    try:
        profile_bot_message = await bot.send_message(
            chat_id=message.chat.id,
            text=profile_message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        await state.update_data(bot_message_id=profile_bot_message.message_id)
        await state.set_state(MenuStates.PROFILE_MENU)
        logger.info("Sent PROFILE_MENU_TEXT")
    except Exception as e:
        logger.error(f"Failed to send profile menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробники для стану PROFILE_MENU та інших профільних станів
@profile_router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_main_menu())
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = MenuStates.PROFILE_MENU

    if user_choice == MenuButton.STATISTICS.value:
        new_main_text = "📊 Меню Статистика"
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Statistics Menu"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = "🏅 Меню Досягнення"
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Achievements Menu"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = "⚙️ Меню Налаштування"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Settings Menu"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = "📝 Меню Зворотного зв'язку"
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Feedback Menu"
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = "❓ Меню Допомоги"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Help Menu"
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.PROFILE_MENU

    # Відправка нового повідомлення з відповідною клавіатурою
    try:
        main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове головне повідомлення: {e}")
        return

    # Видалення старого повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення MLS
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
        logger.info("Successfully edited interactive message to new state description")
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
            logger.info("Sent new interactive message for new state")
        except Exception as e2:
            logger.error(f"Не вдалося відправити інтерактивне повідомлення для нового стану: {e2}")

    await state.set_state(new_state)

# Обробчик зміни імені користувача
@profile_router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    new_username = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is changing username to: {new_username}")
    await message.delete()
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
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробчик отримання зворотного зв'язку
@profile_router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} sent feedback: {feedback}")
    await message.delete()
    if feedback:
        # Збереження зворотного зв'язку у базі даних або надсилання адміністратору
        # Приклад збереження у таблиці Feedback
        # from models.feedback import Feedback
        # new_feedback = Feedback(user_id=user_id, feedback=feedback)
        # db.add(new_feedback)
        # await db.commit()

        response_text = FEEDBACK_RECEIVED_TEXT
        logger.info(f"Feedback received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, надайте ваш зворотний зв'язок."
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробчик повідомлення про помилку
@profile_router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} reported a bug: {bug_report}")
    await message.delete()
    if bug_report:
        # Збереження звіту про помилку у базі даних або надсилання адміністратору
        # Приклад збереження у таблиці BugReports
        # from models.bug_report import BugReport
        # new_bug = BugReport(user_id=user_id, report=bug_report)
        # db.add(new_bug)
        # await db.commit()

        response_text = BUG_REPORT_RECEIVED_TEXT
        logger.info(f"Bug report received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Функція для налаштування обробників з Dispatcher
def setup_handlers(dp: Router):
    dp.include_router(profile_router)
