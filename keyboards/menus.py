# Нові меню для кожної секції

# Меню "Персонажі"
def get_heroes_menu():
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Гайди"
def get_guides_menu():
    return create_menu(
        [
            MenuButton("🆕 Нові Гайди"),
            MenuButton("🌟 Популярні Гайди"),
            MenuButton("📘 Для Початківців"),
            MenuButton("🧙 Просунуті Техніки"),
            MenuButton("🛡️ Командна Гра"),
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Контр-піки"
def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton("🔎 Пошук Контр-піку"),
            MenuButton("📝 Список Персонажів"),
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню "Білди"
def get_builds_menu():
    return create_menu(
        [
            MenuButton("🏗️ Створити Білд"),
            MenuButton("📄 Мої Білди"),
            MenuButton("💎 Популярні Білди"),
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню "Голосування"
def get_voting_menu():
    return create_menu(
        [
            MenuButton("📍 Поточні Опитування"),
            MenuButton("📋 Мої Голосування"),
            MenuButton("➕ Запропонувати Тему"),
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Профіль"
def get_profile_menu():
    return create_menu(
        [
            MenuButton("📊 Загальна Активність"),
            MenuButton("🥇 Рейтинг"),
            MenuButton("🎮 Ігрова Статистика"),
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Досягнення"
def get_achievements_menu():
    return create_menu(
        [
            MenuButton("🎖️ Мої Бейджі"),
            MenuButton("🚀 Прогрес"),
            MenuButton("🏅 Турнірна Статистика"),
            MenuButton("🎟️ Отримані Нагороди"),
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Налаштування"
def get_settings_menu():
    return create_menu(
        [
            MenuButton("🌐 Мова Інтерфейсу"),
            MenuButton("🆔 Змінити Username"),
            MenuButton("🛡️ Оновити ID Гравця"),
            MenuButton("🔔 Сповіщення"),
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Допомога"
def get_help_menu():
    return create_menu(
        [
            MenuButton("📄 Інструкції"),
            MenuButton("❔ FAQ"),
            MenuButton("📞 Підтримка"),
            MenuButton.BACK
        ],
        row_width=1
    )
