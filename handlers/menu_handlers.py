from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional
import logging

# Імпортуємо наші клавіатури
from keyboards.main_menu import MainMenu
from keyboards.navigation import (
    HeroesMenu,
    BuildsMenu,
    GuidesMenu,
    StatisticsMenu
)
from keyboards.cabinet import (
    ProfileMenu,
    SettingsMenu,
    AchievementsMenu
)

logger = logging.getLogger(__name__)

router = Router(name="menu_router")

class MenuStates(StatesGroup):
    main = State()
    heroes = State()
    builds = State()
    guides = State()
    statistics = State()
    profile = State()
    settings = State()
    achievements = State()

class MenuNavigator:
    def __init__(self):
        self.menus = {
            'main': MainMenu(),
            'heroes': HeroesMenu(),
            'builds': BuildsMenu(),
            'guides': GuidesMenu(),
            'statistics': StatisticsMenu(),
            'profile': ProfileMenu(),
            'settings': SettingsMenu(),
            'achievements': AchievementsMenu()
        }

    async def get_menu(self, menu_name: str, user_id: Optional[int] = None) -> tuple:
        """Отримати клавіатуру та текст для конкретного меню"""
        menu = self.menus.get(menu_name)
        if not menu:
            raise ValueError(f"Невідоме меню: {menu_name}")
        
        keyboard = await menu.get_keyboard(user_id)
        text = await menu.get_text(user_id)
        return keyboard, text

menu_navigator = MenuNavigator()

@router.message(Command("menu"))
@router.message(F.text == "🏠 Головне меню")
async def show_main_menu(message: Message, state: FSMContext):
    """Показати головне меню"""
    try:
        keyboard, text = await menu_navigator.get_menu('main')
        await state.set_state(MenuStates.main)
        await message.answer(text, reply_markup=keyboard)
        logger.info(f"Показано головне меню користувачу {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі головного меню: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

@router.callback_query(F.data.startswith("menu_"))
async def handle_menu_navigation(callback: CallbackQuery, state: FSMContext):
    """Обробка навігації по меню"""
    try:
        action = callback.data.split('_')[1]
        user_id = callback.from_user.id
        
        # Перевіряємо, чи є такий пункт меню
        if action not in menu_navigator.menus:
            await callback.answer("Цей розділ в розробці!")
            return

        # Отримуємо клавіатуру та текст для вибраного меню
        keyboard, text = await menu_navigator.get_menu(action, user_id)
        
        # Встановлюємо стан меню
        await state.set_state(getattr(MenuStates, action))
        
        # Оновлюємо повідомлення з новим меню
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
        logger.info(f"Користувач {user_id} перейшов до меню {action}")
    
    except Exception as e:
        logger.error(f"Помилка при навігації по меню: {e}")
        await callback.answer("Виникла помилка. Спробуйте пізніше.", show_alert=True)

@router.callback_query(F.data == "menu_back")
async def handle_menu_back(callback: CallbackQuery, state: FSMContext):
    """Обробка повернення на попереднє меню"""
    try:
        current_state = await state.get_state()
        user_id = callback.from_user.id

        # Визначаємо попереднє меню
        previous_menu = 'main'  # За замовчуванням повертаємося в головне меню
        
        # Отримуємо клавіатуру та текст для попереднього меню
        keyboard, text = await menu_navigator.get_menu(previous_menu, user_id)
        
        # Встановлюємо попередній стан
        await state.set_state(MenuStates.main)
        
        # Оновлюємо повідомлення
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
        logger.info(f"Користувач {user_id} повернувся до попереднього меню")
    
    except Exception as e:
        logger.error(f"Помилка при поверненні до попереднього меню: {e}")
        await callback.answer("Виникла помилка. Спробуйте пізніше.", show_alert=True)

# Додаткові обробники для специфічних дій в меню
@router.callback_query(F.data.startswith("hero_"))
async def handle_hero_selection(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору героя"""
    try:
        hero_id = callback.data.split('_')[1]
        # Тут буде логіка показу інформації про героя
        await callback.answer(f"Інформація про героя {hero_id} в розробці!")
    except Exception as e:
        logger.error(f"Помилка при виборі героя: {e}")
        await callback.answer("Виникла помилка. Спробуйте пізніше.", show_alert=True)

@router.callback_query(F.data.startswith("build_"))
async def handle_build_selection(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору білда"""
    try:
        build_id = callback.data.split('_')[1]
        # Тут буде логіка показу білда
        await callback.answer(f"Білд {build_id} в розробці!")
    except Exception as e:
        logger.error(f"Помилка при виборі білда: {e}")
        await callback.answer("Виникла помилка. Спробуйте пізніше.", show_alert=True)
