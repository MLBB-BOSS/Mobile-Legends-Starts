# handlers/main_menu.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# Імпорт станів із ваших файлів
from states.menu_states import MainMenuState, NavigationState, ProfileState

# Імпорт функцій, що формують клавіатури
from keyboards.menus import (
    get_main_menu_keyboard,
    get_main_menu_inline_keyboard,
    get_navigation_menu,
    get_navigation_inline_keyboard,
    get_profile_menu,
    get_profile_inline_keyboard
)

# Тексти, які точно існують у texts.py
from texts import MAIN_MENU_TEXT

# Інтерфейсні та сервісні утиліти
from utils.interface_manager import safe_delete_message
# BaseHandler містить self.router = Router() і методи, якими користується цей клас
from .base_handler import BaseHandler

# -----------------------------------------
# Тимчасове (або постійне) визначення 
# MAIN_MENU_SCREEN_TEXT, щоб уникнути ImportError.
# Якщо Ви вже додали цю константу до texts.py,
# тоді приберіть її звідси й імпортуйте з texts.py
# -----------------------------------------
MAIN_MENU_SCREEN_TEXT = """\
Вітаємо у головному меню!
Оберіть дію чи розділ нижче...
"""

router = Router()

class MainMenuHandler(BaseHandler):
    def __init__(self):
        """
        При ініціалізації викликаємо батьківський конструктор,
        який створить self.router = Router() та інші потрібні речі.
        """
        super().__init__(name="main_menu")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників головного меню."""
        # Приклад: обробник команди /start
        self.router.message.register(self.cmd_start, CommandStart())
        # Обробник кнопок головного меню (стан MainMenuState.main)
        self.router.message.register(self.handle_main_menu, MainMenuState.main)

    async def cmd_start(self, message: Message, state: FSMContext):
        """
        Обробка команди /start.
        Тут створюємо 2 повідомлення:
        1) "екран" (звичайно містить якесь велике вітання або інфо)
        2) "пульт" (повідомлення з кнопками головного меню)
        """
        # Видаляємо повідомлення користувача
        await safe_delete_message(message.bot, message.chat.id, message.message_id)

        # Створюємо повідомлення-екран
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_inline_keyboard()
        )

        # Створюємо повідомлення-пульт із кнопками
        control = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Встановлюємо стан FSM
        await state.set_state(MainMenuState.main)
        # Зберігаємо ідентифікатори повідомлень та інші дані
        await state.update_data(
            bot_message_id=control.message_id,      # ID "пульта"
            interactive_message_id=screen.message_id,  # ID "екрану"
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """
        Обробка натискання кнопок у головному меню, 
        коли користувач перебуває у стані MainMenuState.main.
        """
        # Текст кнопки, яку натиснув користувач
        user_choice = message.text

        # Варіант обробки через match-case (Python 3.10+)
        match user_choice:
            case "🧭 Навігація":
                # Для переходу в "навігацію" - викликаємо handle_transition,
                # припустимо, у Вас він оголошений у BaseHandler
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=NavigationState.main,
                    control_text="Навігаційне меню\nОберіть розділ:",
                    control_markup=get_navigation_menu_keyboard(),
                    screen_text="🧭 Навігація по грі\n\nТут ви знайдете:\n- Інформацію про героїв\n- Білди та гайди\n- Турніри та �[...]
                    screen_markup=get_navigation_inline_keyboard()
                )

            case "🪪 Мій Профіль":
                # Перехід у меню профілю
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=ProfileState.main,
                    control_text="Меню профілю\nОберіть опцію:",
                    control_markup=get_profile_menu_keyboard(),
                    screen_text="👤 Ваш профіль\n\nТут ви можете:\n- Переглянути статистику\n- Керувати налаштуваннями\n- Переві[...]
                    screen_markup=get_profile_inline_keyboard()
                )

            case _:
                # Якщо натиснуто іншу кнопку (чи неочікуваний ввід),
                # Можна відправити якесь повідомлення чи проігнорувати
                await message.answer("Невідома команда, будь ласка скористайтеся кнопками меню.")
                # У разі потреби залишаємось у тому ж стані