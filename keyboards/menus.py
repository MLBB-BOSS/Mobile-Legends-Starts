# Навігаційне меню
def get_navigation_menu():
    """
    Створює навігаційне меню.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню гайдів
def get_guides_menu():
    """
    Створює меню гайдів.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,  # Можливо, замінити на специфічні кнопки для гайдів
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню контр-піків
def get_counter_picks_menu():
    """
    Створює меню контр-піків.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню білдів
def get_builds_menu():
    """
    Створює меню білдів.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню голосування
def get_voting_menu():
    """
    Створює меню голосування.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,  # Замініть на актуальні кнопки для голосування
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню профілю
def get_profile_menu():
    """
    Створює меню профілю.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,  # Можна замінити на функції профілю, такі як "Статистика" або "Налаштування"
            MenuButton.BACK
        ],
        row_width=1
    )
