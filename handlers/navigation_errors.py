from aiogram import Bot
from aiogram.fsm.context import FSMContext
import logging
from navigation_config import NavigationConfig

logger = logging.getLogger(__name__)

async def handle_navigation_error(bot: Bot, chat_id: int, state: FSMContext):
    """Обробка помилок навігації."""
    try:
        # Надсилаємо повідомлення про помилку користувачеві
        await bot.send_message(
            chat_id=chat_id,
            text=NavigationConfig.Messages.ERROR,
            reply_markup=get_main_menu()
        )
        logger.info(f"Надіслано повідомлення про помилку до чату {chat_id}")
        
        # Встановлюємо стан MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        logger.info(f"Стан встановлено на MAIN_MENU для чату {chat_id}")
        
        # Очищуємо дані стану
        await state.update_data(
            bot_message_id=None,
            interactive_message_id=None,
            last_text="",
            last_keyboard=None
        )
        logger.info(f"Дані стану очищено для чату {chat_id}")

    except Exception as e:
        # Логування критичної помилки
        logger.critical(f"Критична помилка при обробці помилки навігації: {e}")
