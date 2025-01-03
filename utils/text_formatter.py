# utils/text_formatter.py

from typing import Dict

def format_profile_text(template: str, profile_info: Dict[str, any]) -> str:
    """
    Форматує текст профілю користувача з використанням шаблону.

    :param template: Шаблон тексту з місцями для заповнення.
    :param profile_info: Словник з інформацією про профіль.
    :return: Відформатований текст профілю.
    """
    return template.format(**profile_info)
