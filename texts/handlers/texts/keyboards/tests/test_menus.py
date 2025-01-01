# tests/test_menus.py

import pytest
from keyboards.menus import get_main_menu, get_navigation_menu
from texts.enums import MenuButton

def test_get_main_menu():
    main_menu = get_main_menu()
    assert main_menu is not None
    assert len(main_menu.keyboard) == 1  # Одна рядок
    assert len(main_menu.keyboard[0]) == 2  # Дві кнопки
    assert main_menu.keyboard[0][0].text == MenuButton.NAVIGATION.value
    assert main_menu.keyboard[0][1].text == MenuButton.PROFILE.value

def test_get_navigation_menu():
    navigation_menu = get_navigation_menu()
    assert navigation_menu is not None
    expected_buttons = [
        MenuButton.HEROES.value,
        MenuButton.BUILDS.value,
        MenuButton.GUIDES.value,
        MenuButton.TOURNAMENTS.value,
        MenuButton.TEAMS.value,
        MenuButton.CHALLENGES.value,
        MenuButton.BUST.value,
        MenuButton.TRADING.value,
        MenuButton.BACK.value
    ]
    flat_buttons = [btn.text for row in navigation_menu.keyboard for btn in row]
    assert flat_buttons == expected_buttons
