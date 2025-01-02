# handlers/navigation.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import logging

from interface_messages import InterfaceMessages
from navigation_state_manager import NavigationStateManager
from navigation_config import NavigationConfig
from states.menu_states import MenuStates
from keyboards.menus import get_navigation_menu
from utils.message_utils import safe_delete_message, check_and_edit_message

router = Router()
logger = logging.getLogger(__name__)

async def update_interface_messages(
    bot, chat_id: int, old_message_id: int, 
    interactive_message_id: int, state: FSMContext
) -> tuple[int, int]:
    """
    Оновлює інтерфейсні повідомлення. Повертає нові ID повідомлень.
    """
    try:
        # Спробуємо відредагувати існуюче повідомлення
        if old_message_id:
            success = await check_and_edit_message(
                bot=bot,
                chat_id=chat_id,
                message_id=old_message_id,
                text=NavigationConfig.Messages.NAVIGATION_MENU,
                keyboard=get_navigation_menu()
            )
            if success:
                return old_message_id, interactive_message_id

        # Якщо редагування не вдалося, видаляємо старі повідомлення і створюємо нові
        await safe_delete_message(bot, chat_id, old_message_id)
        await safe_delete_message(bot, chat_id, interactive_message_id)

        # Створюємо нове повідомлення
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=NavigationConfig.Messages.NAVIGATION_MENU,
            reply_markup=get_navigation_menu()
        )

        # Створюємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=NavigationConfig.Messages.NAVIGATION_INTERACTIVE,
            reply_markup=get_generic_inline_keyboard()
        )

        return new_message.message_id, new_interactive_message.message_id

    except Exception as e:
        logger.error(f"Помилка при оновленні інтерфейсу: {e}")
        return None, None

async def handle_navigation_error(bot, chat_id: int, state: FSMContext):
    """
    Обробляє помилки навігації.
    """
    try:
        await bot.send_message(
            chat_id=chat_id,
            text="Виникла помилка при навігації. Спробуйте ще раз або зверніться до адміністратора.",
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Помилка при обробці помилки навігації: {e}")

@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext, bot):
    """
    Обробник переходу до навігаційного меню.
    """
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    # Ініціалізація менеджера станів
    state_manager = NavigationStateManager(state)
    await state_manager.load_state()

    try:
        # Видалення повідомлення користувача
        await safe_delete_message(bot, message.chat.id, message.message_id)

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

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_selection(message: Message, state: FSMContext):
    """
    Обробляє вибір опцій в навігаційному меню.
    """
    try:
        text = message.text
        logger.info(f"Користувач {message.from_user.id} вибрав опцію: {text}")

        # Маппінг опцій меню до станів
        menu_options = {
            "🥷 Персонажі": MenuStates.HEROES_MENU,
            "🏆 Турніри": MenuStates.TOURNAMENTS_MENU,
            "📚 Гайди": MenuStates.GUIDES_MENU,
            "🛡️ Білди": MenuStates.BUILDS_MENU,
            "🧑‍🤝‍🧑 Команди": MenuStates.TEAMS_MENU,
            "🧩 Челендж": MenuStates.CHALLENGES_MENU,
            "🚀 Буст": MenuStates.BUST_MENU,
            "💰 Торгівля": MenuStates.TRADING_MENU,
            "🔙 Назад": MenuStates.MAIN_MENU
        }

        if text in menu_options:
            await state.set_state(menu_options[text])
            await message.answer(f"Ви перейшли до розділу {text}")
            logger.info(f"Користувач {message.from_user.id} встановив стан {menu_options[text]}")
        else:
            await message.answer("Невідома опція. Будь ласка, виберіть опцію з меню.")
            logger.warning(f"Користувач {message.from_user.id} вибрав невідому опцію: {text}")

    except Exception as e:
        logger.error(f"Помилка при обробці вибору в навігаційному меню: {e}")
        await handle_navigation_error(message.bot, message.chat.id, state)