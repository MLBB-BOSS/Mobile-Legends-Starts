# File: utils/localization.py

def get_message(self, key: str, **kwargs) -> str:
    self.logger.debug(f"Отримання повідомлення для ключа: {key}")
    try:
        keys = key.split('.')
        value = self.messages
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                self.logger.debug(f"Перейшли до ключа '{k}', значення: {value}")
            else:
                self.logger.warning(f"Очікував dict на ключі '{k}', але отримав {type(value)}")
                return f"Message key '{key}' not found"

            if value is None:
                self.logger.warning(f"Повідомлення для ключа '{key}' не знайдено на '{k}'")
                return f"Message key '{key}' not found"

        if isinstance(value, str):
            formatted_value = value.format(**kwargs)
            self.logger.debug(f"Повертаємо відформатоване повідомлення: {formatted_value}")
            return formatted_value
        elif isinstance(value, dict):
            self.logger.warning(f"Підтримується лише рядковий тип для ключа '{key}', але отримано {type(value)}")
            return f"Message key '{key}' not found"
        else:
            self.logger.warning(f"Непідтримуваний тип для ключа '{key}': {type(value)}")
            return f"Message key '{key}' not found"
    except Exception as e:
        self.logger.error(f"Помилка при отриманні повідомлення для ключа '{key}': {e}")
        return f"Error getting message for key '{key}'"
