from .base_keyboard import BaseKeyboard
from .keyboard_buttons import Buttons, MenuLevel

class MenuKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()
        self._current_level = MenuLevel.MAIN

    def get_main_menu(self):
        self._current_level = MenuLevel.MAIN
        buttons = [
            [Buttons.NAVIGATION.value, Buttons.HEROES.value],
            [Buttons.TOURNAMENTS.value, Buttons.PROFILE.value],
            [Buttons.SETTINGS.value]
        ]
        return self.create_keyboard(buttons, add_back=False, add_main=False)

    def get_navigation_menu(self):
        self._current_level = MenuLevel.NAVIGATION
        buttons = [
            [Buttons.CHARACTERS.value, Buttons.MAPS.value],
            [Buttons.GUIDES.value]
        ]
        return self.create_keyboard(buttons)

    def get_heroes_menu(self):
        self._current_level = MenuLevel.HEROES
        buttons = [
            [Buttons.TANK.value, Buttons.FIGHTER.value],
            [Buttons.ASSASSIN.value, Buttons.MAGE.value],
            [Buttons.MARKSMAN.value, Buttons.SUPPORT.value]
        ]
        return self.create_keyboard(buttons)

    def get_tournaments_menu(self):
        self._current_level = MenuLevel.TOURNAMENTS
        buttons = [
            [Buttons.ACTIVE.value, Buttons.UPCOMING.value],
            [Buttons.PAST.value, Buttons.CREATE.value]
        ]
        return self.create_keyboard(buttons)

    def get_profile_menu(self):
        self._current_level = MenuLevel.PROFILE
        buttons = [
            [Buttons.STATS.value, Buttons.ACHIEVEMENTS.value],
            [Buttons.INVENTORY.value]
        ]
        return self.create_keyboard(buttons)

    def get_settings_menu(self):
        self._current_level = MenuLevel.SETTINGS
        buttons = [
            ["Мова", "Сповіщення"],
            ["Тема", "Приватність"]
        ]
        return self.create_keyboard(buttons)
