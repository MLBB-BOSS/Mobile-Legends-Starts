# utils/messages.py

import json
import os

class Messages:
    _instance = None

    def __new__(cls, filepath='messages.json'):
        if cls._instance is None:
            cls._instance = super(Messages, cls).__new__(cls)
            cls._instance.load_messages(filepath)
        return cls._instance

    def load_messages(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл {filepath} не знайдено.")
        with open(filepath, 'r', encoding='utf-8') as f:
            self.messages = json.load(f)

    def get(self, *keys, **kwargs):
        data = self.messages
        try:
            for key in keys:
                data = data[key]
        except KeyError:
            return "Текст не знайдено."
        if isinstance(data, str):
            return data.format(**kwargs)
        return data
