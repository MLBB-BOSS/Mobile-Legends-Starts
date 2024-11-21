# File: test_localization.py

from utils.localization_instance import loc

def test_localization():
    keys = [
        "buttons.navigation",
        "buttons.voting",
        "buttons.profile",
        "messages.start_command",
        "messages.navigation_menu",
        "messages.select_hero_class",
        "messages.guides_menu",
        "messages.counter_picks_menu",
        "messages.builds_menu",
        "messages.voting_menu",
        "messages.profile_menu",
        "messages.menu_welcome",
        "messages.unhandled_message"
    ]

    for key in keys:
        message = loc.get_message(key)
        print(f"{key}: {message}")

if __name__ == "__main__":
    test_localization()
