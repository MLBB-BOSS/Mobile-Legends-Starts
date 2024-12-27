from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    # 1-20: Основне меню
    MAIN_MENU = State()                 # 1. Головне меню користувача
    CHALLENGES_MENU = State()           # 2. Меню викликів
    GUIDES_MENU = State()               # 3. Меню посібників
    BUST_MENU = State()                 # 4. Меню BUST
    TEAMS_MENU = State()                # 5. Меню команд
    TRADING_MENU = State()              # 6. Меню торгівлі
    SETTINGS_MENU = State()             # 7. Меню налаштувань
    SETTINGS_SUBMENU = State()          # 8. Підменю налаштувань
    SELECT_LANGUAGE = State()           # 9. Вибір мови
    PROFILE_MENU = State()              # 10. Меню профілю
    STATS_MENU = State()                # 11. Меню статистики
    ACHIEVEMENTS_MENU = State()          # 12. Меню досягнень
    FEEDBACK_MENU = State()             # 13. Меню зворотного зв'язку
    HELP_MENU = State()                 # 14. Меню довідки
    MY_TEAM_MENU = State()              # 15. Меню моєї команди
    GPT_MENU = State()                  # 16. Меню GPT
    HELP_SUBMENU = State()              # 17. Підменю довідки
    CHANGE_USERNAME = State()           # 18. Зміна імені користувача
    RECEIVE_FEEDBACK = State()          # 19. Отримання зворотного зв'язку
    REPORT_BUG = State()                # 20. Повідомлення про помилку

    # 21-26: Раніше запропоновані стани
    TOURNAMENTS_MENU = State()          # 21. Меню турнірів
    HEROES_MENU = State()               # 22. Меню героїв
    COUNTER_PICKS_MENU = State()        # 23. Меню контрпічів
    BUILDS_MENU = State()               # 24. Меню збірок
    VOTING_MENU = State()               # 25. Меню голосування
    NAVIGATION_MENU = State()           # 26. Меню навігації

    # 27-28: Нові стани
    META_MENU = State()                 # 27. Меню мета-ігри
    M6_MENU = State()                   # 28. Меню секції M6

    # 29-32: Додаткові стани, знайдені в обробниках
    HERO_LIST_MENU = State()            # 29. Меню списку героїв у мета-меню
    RECOMMENDATIONS_MENU = State()       # 30. Меню рекомендацій у мета-меню
    UPDATES_MENU = State()              # 31. Меню оновлень у мета-меню
    BACK_TO_MAIN = State()              # 32. Повернення до головного меню

    # 33-35: Стани порівняння героїв
    COMPARISON_STEP_1 = State()         # 33. Вибір першого героя/предмета для порівняння
    COMPARISON_STEP_2 = State()         # 34. Вибір другого героя/предмета для порівняння
    COMPARISON_RESULT = State()         # 35. Показ результатів порівняння

    # 36-43: Стани пошуку та управління героями
    SEARCH_HERO = State()               # 36. Стан пошуку героя
    HERO_DETAILS = State()              # 37. Перегляд деталей героя
    HERO_SELECTION = State()            # 38. Вибір героя зі списку
    HERO_FILTER = State()               # 39. Фільтрація героїв
    HERO_SORT = State()                 # 40. Сортування героїв
    HERO_FAVORITES = State()            # 41. Обрані герої
    HERO_STATISTICS = State()           # 42. Статистика героя
    HERO_CLASS_MENU = State()           # 43. Меню класів героїв

    # 44-49: Стани системи пошуку
    SEARCH_TOPIC = State()              # 44. Пошук за темою
    SEARCH_CATEGORY = State()           # 45. Пошук за категорією
    SEARCH_RESULT = State()             # 46. Результати пошуку
    SEARCH_FILTER = State()             # 47. Фільтрація пошуку
    SEARCH_HISTORY = State()            # 48. Історія пошуку
    SEARCH_FAVORITES = State()          # 49. Обрані пошукові запити

    # 50-56: Стани системи турнірів
    TOURNAMENT_CREATE = State()         # 50. Створення турніру
    TOURNAMENT_EDIT = State()           # 51. Редагування турніру
    TOURNAMENT_JOIN = State()           # 52. Приєднання до турніру
    TOURNAMENT_LIST = State()           # 53. Список турнірів
    TOURNAMENT_BRACKET = State()        # 54. Блок-діаграма турніру
    TOURNAMENT_RESULTS = State()        # 55. Результати турніру
    TOURNAMENT_RULES = State()          # 56. Правила турніру

    # 57-62: Стани управління командами
    TEAM_CREATE = State()               # 57. Створення команди
    TEAM_EDIT = State()                # 58. Редагування команди
    TEAM_INVITE = State()              # 59. Запрошення до команди
    TEAM_ROSTER = State()              # 60. Список гравців команди
    TEAM_SETTINGS = State()            # 61. Налаштування команди
    TEAM_STATS = State()               # 62. Статистика команди

    # 63-67: Стани матчів
    MATCH_CREATE = State()             # 63. Створення матчу
    MATCH_JOIN = State()               # 64. Приєднання до матчу
    MATCH_RESULT = State()             # 65. Результат матчу
    MATCH_HISTORY = State()            # 66. Історія матчів
    MATCH_REPORT = State()             # 67. Звіт про матч

    # 68-71: Стани управління контентом
    CONTENT_CREATE = State()           # 68. Створення контенту
    CONTENT_EDIT = State()             # 69. Редагування контенту
    CONTENT_DELETE = State()           # 70. Видалення контенту
    CONTENT_REVIEW = State()           # 71. Рецензування контенту

    # 72-74: Стани системи досягнень
    ACHIEVEMENT_VIEW = State()         # 72. Перегляд досягнень
    ACHIEVEMENT_PROGRESS = State()     # 73. Прогрес досягнень
    ACHIEVEMENT_CLAIM = State()        # 74. Отримання досягнення

    # 75-77: Стани спільноти
    COMMUNITY_CHAT = State()           # 75. Чат спільноти
    COMMUNITY_EVENTS = State()         # 76. Події спільноти
    COMMUNITY_RULES = State()          # 77. Правила спільноти

    # 78-79: Стани сповіщень
    NOTIFICATIONS_SETTINGS = State()    # 78. Налаштування сповіщень
    NOTIFICATIONS_LIST = State()        # 79. Список сповіщень

    # 80-82: Стани системи звітів
    REPORT_CREATE = State()            # 80. Створення звіту
    REPORT_DETAILS = State()           # 81. Деталі звіту
    REPORT_STATUS = State()            # 82. Статус звіту

    # 83-86: Стани системи посібників
    GUIDE_CREATE = State()             # 83. Створення посібника
    GUIDE_EDIT = State()               # 84. Редагування посібника
    GUIDE_VIEW = State()               # 85. Перегляд посібника
    GUIDE_LIST = State()               # 86. Список посібників

    # 87-89: Стани аналітики
    ANALYTICS_OVERVIEW = State()       # 87. Загальний огляд аналітики
    ANALYTICS_DETAILED = State()       # 88. Деталізована аналітика
    ANALYTICS_EXPORT = State()         # 89. Експорт аналітики

    # 90-92: Стани управління скріншотами
    SCREENSHOT_UPLOAD = State()        # 90. Завантаження скріншоту
    SCREENSHOT_REVIEW = State()        # 91. Рецензування скріншоту
    SCREENSHOT_GALLERY = State()       # 92. Галерея скріншотів

    # 93-95: Стани підтримки
    SUPPORT_TICKET = State()           # 93. Квиток підтримки
    SUPPORT_CHAT = State()             # 94. Чат підтримки
    SUPPORT_FAQ = State()              # 95. Часті запитання підтримки

    # 96-99: Intro states
    INTRO_PAGE_1 = State()            # 96. Перша сторінка вступу
    INTRO_PAGE_2 = State()            # 97. Друга сторінка вступу
    INTRO_PAGE_3 = State()            # 98. Третя сторінка вступу
    INTRO_COMPLETE = State()          # 99. Завершення вступу

    MAIN_MENU = "main_menu"
    FEEDBACK = "feedback"
    RATING = "rating"
    SUGGESTION = "suggestion"
    REPORT = "report"
