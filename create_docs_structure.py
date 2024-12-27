"""
Script to automatically create documentation structure for MLBB-BOSS project.
"""

import os
from pathlib import Path
from typing import Dict, List

# Structure definition
DOCS_STRUCTURE: Dict[str, List[str]] = {
    "guide": [
        "getting-started.md",
        "commands.md",
        "tournaments.md"
    ],
    "api": [
        "handlers.md",
        "utils.md",
        "database.md"
    ],
    "development": [
        "contributing.md",
        "architecture.md"
    ]
}

# Template content for different types of files
TEMPLATES = {
    "index.md": """# MLBB-BOSS Documentation

Ласкаво просимо до документації MLBB-BOSS - бота для організації турнірів Mobile Legends!

## Можливості

- Організація турнірів
- Управління учасниками
- Збереження скріншотів
- Система досягнень
- Статистика гравців

## Швидкий старт

1. Додайте бота до вашої групи
2. Використовуйте команду /start
3. Слідуйте інструкціям для налаштування

## Корисні посилання

- [Початок роботи](guide/getting-started.md)
- [Команди бота](guide/commands.md)
- [API документація](api/handlers.md)
""",
    "guide/getting-started.md": """# Початок роботи

## Встановлення бота

1. Додайте бота до вашої групи
2. Надайте необхідні права
3. Виконайте початкове налаштування

## Базові команди

- `/start` - Почати роботу з ботом
- `/help` - Отримати довідку
- `/tournament` - Створити новий турнір
""",
    "guide/commands.md": """# Команди бота

## Загальні команди

- `/start` - Початок роботи
- `/help` - Довідка
- `/settings` - Налаштування

## Команди турніру

- `/tournament create` - Створити турнір
- `/tournament list` - Список турнірів
- `/tournament join` - Приєднатися до турніру
""",
    "api/handlers.md": """# Handlers API

## MessageHandler

Основний клас для обробки повідомлень.

```python
class MessageHandler:
    '''
    Обробник повідомлень бота.
    '''
    pass
