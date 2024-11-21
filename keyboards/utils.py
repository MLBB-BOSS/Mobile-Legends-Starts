def chunk_buttons(buttons: list, chunk_size: int) -> list:
    """Розбиває кнопки на блоки."""
    return [buttons[i:i + chunk_size] for i in range(0, len(buttons), chunk_size)]
