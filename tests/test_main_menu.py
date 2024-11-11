# tests/test_main_menu.py

from your_module import get_main_menu

def test_get_main_menu():
    меню = get_main_menu()
    assert isinstance(меню, dict), f"Очікувався тип dict, отримано {type(меню)}."
    assert "home" in меню, "Ключ 'home' відсутній у меню."
    assert "about" in меню, "Ключ 'about' відсутній у меню."
    assert "contact" in меню, "Ключ 'contact' відсутній у меню."
