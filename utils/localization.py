import json
import os

class Localization:
    def __init__(self, locale='uk'):
        self.locale = locale
        self.messages = self.load_messages()

    def load_messages(self):
        path = os.path.join('utils', 'messages', f'{self.locale}.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл локалізації {path} не знайдено.")

    def get_message(self, key):
        keys = key.split('.')
        message = self.messages
        for k in keys:
            message = message.get(k)
            if message is None:
                return ''
        return message

loc = Localization()
