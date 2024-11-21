# keyboards/menu_keyboard.py
from .base_keyboard import BaseKeyboard
from .keyboard_buttons import Buttons, MenuLevel

class MenuKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()
        self._current_level = MenuLevel.MAIN
        
    def get_main_menu(self):
        self._current_level = MenuLevel.MAIN
        buttons = [
            [Buttons.NAVIGATION, Buttons.HEROES],
            [Buttons.TOURNAMENTS, Buttons.PROFILE],
            [Buttons.SETTINGS]
        ]
        return self.create_keyboard(buttons, add_back=False, add_main=False)
        
    def get_navigation_menu(self):
        self._current_level = MenuLevel.NAVIGATION
        buttons = [
            [Buttons.CHARACTERS, Buttons.MAPS],
            [Buttons.GUIDES]
        ]
        return self.create_keyboard(buttons)
        
    def get_heroes_menu(self):
        self._current_level = MenuLevel.HEROES
        buttons = [
            [Buttons.TANK, Buttons.FIGHTER],
            [Buttons.ASSASSIN, Buttons.MAGE],
            [Buttons.MARKSMAN, Buttons.SUPPORT]
        ]
        return self.create_keyboard(buttons)
        
    def get_tournaments_menu(self):
        self._current_level = MenuLevel.TOURNAMENTS
        buttons = [
            [Buttons.ACTIVE, Buttons.UPCOMING],
            [Buttons.PAST, Buttons.CREATE]
        ]
        return self.create_keyboard(buttons)
        
    def get_profile_menu(self):
        self._current_level = MenuLevel.PROFILE
        buttons = [
            [Buttons.STATS, Buttons.ACHIEVEMENTS],
            [Buttons.INVENTORY]
        ]
        return self.create_keyboard(buttons)
