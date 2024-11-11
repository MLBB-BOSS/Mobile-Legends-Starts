# tests/test_main_menu.py

from handlers.main_menu import get_main_menu

def test_get_main_menu():
    menu = get_main_menu()
    assert isinstance(menu, dict)
    assert 'buttons' in menu
    assert len(menu['buttons']) > 0# Тести для головного меню
