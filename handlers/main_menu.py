# handlers/main_menu.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

# Припускаємо, що states/menu_states.py існує
from states.menu_states import MainMenuState, NavigationState, ProfileState

# Імпортуємо функції для клавіатур, які реально існують у keyboards/menus.py
# За потреби підлаштуйте під фактичні назви функцій у Вашому menus.py
from keyboards.menus import (
    get_main_menu_keyboard,
    get_main_menu_inline_keyboard,
    get_navigation_menu,          # Reply-клавіатура навігації
    get_navigation_inline_keyboard,  # Інлайн-клавіатура навігації
    get_profile_menu,
    get_profile_inline_keyboard
)

# Тексти (як приклад). Якщо MAIN_MENU_TEXT є у texts.py, імпортуйте звідти
from texts import MAIN_MENU_TEXT

# Сервісні утиліти
from utils.interface_manager import safe_delete_message
# Ваш клас BaseHandler, де self.router = Router() і т.д.
from .base_handler import BaseHandler

# -----------------------------------------
# Тимчасова (або постійна) константа:
# -----------------------------------------
MAIN_MENU_SCREEN_TEXT = """\
Вітаємо у головному меню!
Оберіть дію чи розділ нижче...
"""

# Якщо Ви хочете, щоби router був оголошений прямо тут,
# можете використати його безпосередньо. Але в коді видно,
# що Ви успадковуєте BaseHandler, де теж є self.router.
# Можна так:
router = Router()

class MainMenuHandler(BaseHandler):
    def __init__(self):
        """
        При ініціалізації викликаємо батьківський конструктор,
        який створить self.router = Router() та інше.
        """
        super().__init__(name="main_menu")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників для головного меню."""
        # Обробник /start
        self.router.message.register(self.cmd_start, CommandStart())

        # Обробник кнопок у стані MainMenuState.main
        self.router.message.register(self.handle_main_menu, MainMenuState.main)

    async def cmd_start(self, message: Message, state: FSMContext):
        """
        Обробка команди /start: створюємо 2 повідомлення:
         1) "екран" (з інлайн-клавіатурою / вітанням)
         2) "пульт" (reply-клавіатура з головним меню)
        """
        # Видаляємо початкове повідомлення користувача
        await safe_delete_message(message.bot, message.chat.id, message.message_id)

        # "Екран" — повідомлення з інлайн-клавіатурою (як приклад)
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_inline_keyboard()
        )

        # "Пульт" — повідомлення з reply-клавіатурою (головне меню)
        control = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Встановлюємо стан
        await state.set_state(MainMenuState.main)
        # Зберігаємо ID повідомлень у стан
        await state.update_data(
            bot_message_id=control.message_id,        # ID пульта
            interactive_message_id=screen.message_id, # ID екрану
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """
        Обробляє натискання кнопок головного меню,
        доки користувач у стані MainMenuState.main.
        """
        user_choice = message.text

        # match-case (Python 3.10+). Якщо Ви маєте <3.10, замініть на if-elif
        match user_choice:
            case "🧭 Навігація":
                # Переходимо до "навігаційного" стану
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=NavigationState.main,
                    control_text="Навігаційне меню\nОберіть розділ:",
                    control_markup=get_navigation_menu(),  # Reply-клавіатура
                    screen_text=(
                        "🧭 Навігація по грі\n\n"
                        "Тут ви знайдете:\n"
                        "- Інформацію про героїв\n"
                        "- Білди та гайди\n"
                        "- Турніри та інші активності"
                    ),
                    screen_markup=get_navigation_inline_keyboard() # Інлайн-клавіатура
                )

            case "🪪 Мій Профіль":
                # Переходимо до профілю
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=ProfileState.main,
                    control_text="Меню профілю\nОберіть опцію:",
                    control_markup=get_profile_menu(),   # Reply-клавіатура профілю
                    screen_text=(
                        "👤 Ваш профіль\n\n"
                        "Тут ви можете:\n"
                        "- Переглянути статистику\n"
                        "- Керувати налаштуваннями\n"
                        "- Перевірити досягнення"
                    ),
                    screen_markup=get_profile_inline_keyboard() # Інлайн-клавіатура профілю
                )

            case _:
                # Якщо натиснуто якусь кнопку, що не передбачена
                await message.answer("Невідома команда, скористайтеся кнопками меню.")

                # За бажання можна лишатися в тому ж стані
                # (тобто нічого більше не змінювати).