# handlers/navigation.py
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging
from interface_messages import InterfaceMessages
from navigation_state_manager import NavigationStateManager
from navigation_config import NavigationConfig
from states.menu_states import MenuStates  # Додайте цей імпорт
from keyboards.menus import get_navigation_menu  # Додайте цей імпорт, якщо він ще не доданий

router = Router()
logger = logging.getLogger(__name__)

@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    """Обробник переходу до навігаційного меню."""
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    # Ініціалізація менеджера станів
    state_manager = NavigationStateManager(state)
    await state_manager.load_state()

    try:
        # Видалення повідомлення користувача
        if not await safe_delete_message(bot, message.chat.id, message.message_id):
            logger.warning(f"Не вдалося видалити повідомлення користувача {message.message_id}")

        # Оновлення інтерфейсу
        new_message_id, new_interactive_id = await update_interface_messages(
            bot=bot,
            chat_id=message.chat.id,
            old_message_id=state_manager.messages.bot_message_id,
            interactive_message_id=state_manager.messages.interactive_message_id,
            state=state
        )

        if new_message_id and new_interactive_id:
            # Оновлення даних повідомлень
            await state_manager.messages.update(
                bot=bot,
                chat_id=message.chat.id,
                new_message_id=new_message_id,
                new_interactive_id=new_interactive_id,
                text=NavigationConfig.Messages.NAVIGATION_MENU,
                keyboard=get_navigation_menu()
            )
            
            # Перехід до нового стану
            await state_manager.transition_to(MenuStates.NAVIGATION_MENU)
            logger.info(f"Успішний перехід до навігаційного меню для користувача {message.from_user.id}")
        else:
            raise ValueError("Не вдалося оновити інтерфейс")

    except Exception as e:
        logger.error(f"Помилка при переході до навігаційного меню: {e}")
        await handle_navigation_error(bot, message.chat.id, state)
