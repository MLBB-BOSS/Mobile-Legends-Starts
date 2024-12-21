# utils/text_formatter.py

def format_profile_text(template: str, data: dict) -> str:
    """
    Форматує текст профілю, замінюючи плейсхолдери на реальні дані користувача.
    :param template: Шаблонний текст з плейсхолдерами.
    :param data: Словник з даними користувача.
    :return: Відформатований текст.
    """
    try:
        return template.format(**data)
    except KeyError as e:
        missing_key = e.args[0]
        raise ValueError(f"Відсутній ключ для форматування тексту профілю: {missing_key}") from e
