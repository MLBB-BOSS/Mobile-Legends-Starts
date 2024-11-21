# utils/localization_instance.py

class Localization:
    def __init__(self):
        self.messages = {
            "buttons.navigation": "Navigation",
            "buttons.characters": "Characters",
            "messages.select_hero_class": "Please select a hero class",
            # Add other message keys and translations here
        }

    def get_message(self, key):
        return self.messages.get(key, "Message not found")

loc = Localization()
