"states/menu_states.py

from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    """Стани меню бота"""
    
    # Початкові стани
    START = State()        # Початковий стан
    INTRO = State()        # Стан показу інтро
    MAIN_MENU = State()    # Головне меню
    
    # Навігаційні стани
    NAVIGATION_MENU = State()  # Меню навігації
    HEROES_MENU = State()      # Меню героїв
    MAP_MENU = State()         # Меню карти
    ITEMS_MENU = State()       # Меню предметів
    RANKS_MENU = State()       # Меню рангів
    GUIDES_MENU = State()      # Меню гайдів
    META_MENU = State()        # Меню мети
    
    # Стани профілю
    PROFILE_MENU = State()     # Меню профілю
    PROFILE_EDIT = State()     # Редагування профілю"
 https://github.com/copilot/c/f58e0ab1-bf1f-4a31-a15c-3b9643c175dc#:~:text=states/menu_states.py%0A%0Afrom,State()%20%20%20%20%20%23%20%D0%A0%D0%B5%D0%B4%D0%B0%D0%B3%D1%83%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F%20%D0%BF%D1%80%D0%BE%D1%84%D1%96%D0%BB%D1%8E
