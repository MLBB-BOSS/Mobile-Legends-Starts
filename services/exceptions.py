class MLBBBaseException(Exception):
    """Базовий клас для всіх виключень бота"""
    def __init__(self, message: str = None):
        self.message = message or "Сталася невідома помилка"
        super().__init__(self.message)

class ValidationError(MLBBBaseException):
    """Виключення для помилок валідації введення користувача"""
    def __init__(self, message: str = None):
        super().__init__(message or "Некоректні дані")

class DatabaseError(MLBBBaseException):
    """Виключення для помилок бази даних"""
    def __init__(self, message: str = None):
        super().__init__(message or "Помилка бази даних")

class ScreenshotError(MLBBBaseException):
    """Виключення для помилок при роботі зі скріншотами"""
    def __init__(self, message: str = None):
        super().__init__(message or "Помилка при обробці скріншота")

class HeroNotFoundError(MLBBBaseException):
    """Виключення, коли героя не знайдено"""
    def __init__(self, hero_name: str):
        super().__init__(f"Героя '{hero_name}' не знайдено")

class UserNotFoundError(MLBBBaseException):
    """Виключення, коли користувача не знайдено"""
    def __init__(self, user_id: int):
        super().__init__(f"Користувача з ID {user_id} не знайдено")

class PermissionError(MLBBBaseException):
    """Виключення для помилок доступу"""
    def __init__(self, message: str = None):
        super().__init__(message or "Недостатньо прав для виконання операції")

class RateLimitError(MLBBBaseException):
    """Виключення для обмеження частоти запитів"""
    def __init__(self, retry_after: int = None):
        message = "Перевищено ліміт запитів"
        if retry_after:
            message += f". Спробуйте через {retry_after} секунд"
        super().__init__(message)

class InvalidFormatError(ValidationError):
    """Виключення для неправильного формату даних"""
    def __init__(self, expected_format: str):
        super().__init__(f"Неправильний формат. Очікується: {expected_format}")

class DuplicateError(MLBBBaseException):
    """Виключення для дублікатів"""
    def __init__(self, entity_type: str, identifier: str):
        super().__init__(f"{entity_type} з ідентифікатором '{identifier}' вже існує")
