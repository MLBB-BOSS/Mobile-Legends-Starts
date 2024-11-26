def get_characters_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["🗡️ Бійці", "🏹 Стрільці", "🔮 Маги"]),
        create_buttons(["🛡️ Танки", "🏥 Саппорти", "🗲 Гібриди"]),
        create_buttons(["🔥 Метові", "◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть тип героя"
    )
    return keyboard
