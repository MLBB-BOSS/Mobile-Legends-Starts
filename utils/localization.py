import json
import os

class Localization:
    def __init__(self, locale='uk'):
        self.locale = locale
        self.messages = self.load_messages()

    def load_messages(self):
        path = os.path.join('utils', 'messages', f'{self.locale}.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_message(self, key):
        return self.messages.get(key, '')

loc = Localization()
