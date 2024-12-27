Схоже, що виникла помилка імпорту у вашому файлі `bot.py`. Помилка говорить про те, що функція `get_m6_menu` не може бути імпортована з файлу `keyboards/menus.py`.

### Кроки для вирішення проблеми:

1. **Перевірте наявність функції `get_m6_menu` у файлі `keyboards/menus.py`**:
    - Переконайтеся, що функція `get_m6_menu` дійсно існує у файлі `keyboards/menus.py`.
    - Переконайтеся, що ім'я функції написано правильно.

### Приклад перевірки файлу `keyboards/menus.py`

```python
# keyboards/menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_m6_menu():
    """
    Створює меню M6.

    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.M6_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK
        ],
        placeholder="Оберіть інформацію про M6",
        row_width=3
    )

# Інші функції
```

### Приклад перевірки імпорту у файлі `base.py`

```python
# handlers/base.py

from keyboards.menus import get_m6_menu
# Інші імпорти

# Використання функції get_m6_menu у вашому коді
```

### Що робити, якщо функції немає?

Якщо функція `get_m6_menu` дійсно відсутня у файлі `keyboards/menus.py`, додайте її туди, як показано вище. Потім спробуйте знову запустити ваш бот.

### Запуск бота знову

Якщо ви внесли зміни, не забудьте перезапустити ваш бот на Heroku або іншій платформі розгортання.

```sh
git add .
git commit -m "Fixed import error for get_m6_menu"
git push heroku main
```

Це має вирішити проблему з імпортом. Якщо у вас виникнуть додаткові питання або проблеми, будь ласка, дайте мені знати!