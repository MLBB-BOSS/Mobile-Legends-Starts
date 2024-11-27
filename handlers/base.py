# handlers/base.py

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_hero_class_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    heroes_by_class,
)

from keyboards.inline_menus import get_generic_inline_keyboard

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = Router()

# Визначаємо стани меню
class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"👋 Вітаємо, {user_name}, у Mobile Legends Tournament Bot!\n\n"
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Головне Меню
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "🧭 Навігація"
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Герої")
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    await message.answer(
        "Виберіть розділ гайдів:",
        reply_markup=get_guides_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    await message.answer(
        "Виберіть опцію контр-піків:",
        reply_markup=get_counter_picks_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    await message.answer(
        "Виберіть опцію білдів:",
        reply_markup=get_builds_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_main_menu_from_navigation(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до Головного Меню:",
        reply_markup=get_main_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "🛡️ Герої"
@router.message(MenuStates.HEROES_MENU, F.text.in_([
    MenuButton.SEARCH_HERO.value,
    MenuButton.TANK.value,
    MenuButton.MAGE.value,
    MenuButton.MARKSMAN.value,
    MenuButton.ASSASSIN.value,
    MenuButton.SUPPORT.value,
    MenuButton.FIGHTER.value,
    MenuButton.COMPARISON.value
]))
async def cmd_hero_class(message: Message, state: FSMContext):
    hero_class = menu_button_to_class.get(message.text)
    if hero_class:
        logger.info(f"Користувач {message.from_user.id} обрав клас {hero_class}")
        await state.set_state(MenuStates.HERO_CLASS_MENU)
        await state.update_data(hero_class=hero_class)  # Зберігаємо клас героя в стані
        await message.answer(
            f"Виберіть героя з класу {hero_class}:",
            reply_markup=get_hero_class_menu(hero_class)
        )
        # Відправляємо повідомлення з інлайн-кнопками
        await message.answer(
            "Ось ваші інлайн-опції:",
            reply_markup=get_generic_inline_keyboard()
        )
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(
            "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
            reply_markup=get_heroes_menu(),
        )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Героя")
    await message.answer(
        "Будь ласка, введіть ім'я героя для пошуку:",
    )
    # Можна додати стан для пошуку героя
    # Наприклад, створити новий стан, наприклад, SEARCHING_HERO
    # і обробити введений текст у окремому обробнику

# Обробники для вибору героя з класу
all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(MenuStates.HERO_CLASS_MENU, F.text.in_(all_heroes))
async def cmd_select_hero(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HERO_CLASS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_hero_class(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до Профілю:",
        reply_markup=get_profile_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Обробники для інлайн-кнопок
@router.callback_query(F.data == "button1")
async def handle_button1(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 1")
    await call.answer()

@router.callback_query(F.data == "button2")
async def handle_button2(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 2")
    await call.answer()

# Приклади обробників для нових кнопок
# Приклад для кнопки "✏️ Відгук"
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.SEND_FEEDBACK.value)
async def cmd_send_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Надіслати Відгук")
    await message.answer("Будь ласка, напишіть ваш відгук:")
    # Встановіть новий стан, якщо потрібно
    # await state.set_state(MenuStates.SENDING_FEEDBACK)

# Приклад для кнопки "🐛 Повідомити про Баг"
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.REPORT_BUG.value)
async def cmd_report_bug(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Повідомити про Баг")
    await message.answer("Будь ласка, опишіть знайдений баг:")
    # Встановіть новий стан, якщо потрібно
    # await state.set_state(MenuStates.REPORTING_BUG)

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
    elif current_state == MenuStates.HEROES_MENU.state:
        reply_markup = get_heroes_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        reply_markup = get_hero_class_menu(hero_class)
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=reply_markup,
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
