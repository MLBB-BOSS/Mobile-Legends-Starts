@router.callback_query(lambda c: c.data == "general_activity")
async def show_general_activity(callback: types.CallbackQuery):
    # Приклад даних
    text = (
        "🎯 *Загальна Активність:*\n\n"
        "- 📸 *Скріншоти:* 50\n"
        "- 🎯 *Місії:* 20\n"
        "- 🧩 *Вікторини:* 10\n"
        "- 🏆 *Рейтинг:* Топ-25\n"
        "- 📅 *Днів Активності:* 120\n"
        "- 💬 *Повідомлень:* 250"
    )
    await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "game_stats")
async def show_game_stats(callback: types.CallbackQuery):
    # Приклад даних
    text = (
        "🎮 *Ігрова Статистика:*\n\n"
        "- 🥷 *Улюблений Герой:* Karina\n"
        "- 🛡️ *Переглянуті Герої:* 15\n"
        "- ⚙️ *Створені Білди:* 10\n"
        "- 🔮 *Переглянуті Спели:* 20\n"
        "- 🌟 *Турнірні Участі:* 5\n"
        "- 🏅 *Турнірні Перемоги:* 2"
    )
    await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "achievements")
async def show_achievements(callback: types.CallbackQuery):
    # Приклад даних
    text = (
        "🎖️ *Досягнення:*\n\n"
        "- 🏅 *Бейджів:* 7\n"
        "- 📈 *Прогрес до рівня 'Майстер':*\n"
        "  - 📸 Скріншоти: █████░░░░ 50/100\n"
        "  - 🎯 Місії: ███░░░░░░ 20/50\n"
        "  - 🧩 Вікторини: ██░░░░░░ 10/25\n"
        "- 🏆 *Рівень:* Досвідчений"
    )
    await callback.message.edit_text(text, reply_markup=statistics_inline(), parse_mode="Markdown")
