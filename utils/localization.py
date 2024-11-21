import json
import os

class Localization:
    def __init__(self, lang="uk"):
        self.lang = lang
        self.messages = self.load_locale()

    def load_locale(self):
        path = f"config/locales/{self.lang}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_message(self, key: str):
        return self.messages.get(key, f"[{key}]")
