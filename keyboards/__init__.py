# keyboards/__init__.py

# Базовий імпорт без зірочки
from .menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_profile_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    get_tournaments_menu,
    get_meta_menu,
    get_m6_menu,
    get_gpt_menu,
    get_teams_menu,
    get_trading_menu,
    get_challenges_menu,
    get_bust_menu,
    get_my_team_menu,
    get_language_menu,
    get_hero_class_menu,
    get_hero_class_reply_menu,
    MenuButton,
    LanguageButton,
    heroes_by_class,
    menu_button_to_class,
    create_menu
)

from .inline_keyboards import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
    get_back_to_main_menu_button,
    get_inline_main_menu
)

import logging
logger = logging.getLogger(__name__)
logger.info("Keyboards module initialized")

__all__ = [
    # Reply клавіатури
    'get_main_menu',
    'get_navigation_menu',
    'get_heroes_menu',
    'get_profile_menu',
    'get_guides_menu',
    'get_counter_picks_menu',
    'get_builds_menu',
    'get_voting_menu',
    'get_statistics_menu',
    'get_achievements_menu',
    'get_settings_menu',
    'get_feedback_menu',
    'get_help_menu',
    'get_tournaments_menu',
    'get_meta_menu',
    'get_m6_menu',
    'get_gpt_menu',
    'get_teams_menu',
    'get_trading_menu',
    'get_challenges_menu',
    'get_bust_menu',
    'get_my_team_menu',
    'get_language_menu',
    'get_hero_class_menu',
    'get_hero_class_reply_menu',
    
    # Inline клавіатури
    'get_generic_inline_keyboard',
    'get_intro_page_1_keyboard',
    'get_intro_page_2_keyboard',
    'get_intro_page_3_keyboard',
    'get_back_to_main_menu_button',
    'get_inline_main_menu',
    
    # Базові класи та утиліти
    'MenuButton',
    'LanguageButton',
    'heroes_by_class',
    'menu_button_to_class',
    'create_menu'
]
