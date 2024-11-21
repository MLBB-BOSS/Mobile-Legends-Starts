import json
import os


class Localization:
    def __init__(self, locale='uk'):
        self.locale = locale
        self.messages = self.load_messages()

    def load_messages(self):
        # Використання абсолютного шляху
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, '..', 'config', 'messages', 'locales', f'{self.locale}.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл локалізації {path} не знайдено.")

    def get_message(self, key, **kwargs):
        """
        Get a localized message with optional parameter substitution.
        
        Args:
            key (str): The dot-separated path to the message
            **kwargs: Variables to substitute in the message
        """
        keys = key.split('.')
        message = self.messages
        for k in keys:
            message = message.get(k)
            if message is None:
                return "Помилка: повідомлення не знайдено"
        
        # If we have a string message and kwargs, try to format it
        if isinstance(message, str) and kwargs:
            try:
                return message.format(**kwargs)
            except KeyError as e:
                logger.error(f"Missing key in message format: {e}")
                return message
        return message


# Example initialization
loc = Localization()
