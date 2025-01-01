from aiogram.fsm.state import State, StatesGroup

class HeroStates(StatesGroup):
    """
    Стани FSM для роботи з героями.
    """
    # Основний стан вибору героя
    main = State()

    # Вибір класу героя
    class_selection = State()

    # Вибір конкретного героя з класу
    hero_selection = State()

    # Перегляд детальної інформації про героя
    hero_info = State()

    # Порівняння героїв
    comparison_step_1 = State()
    comparison_step_2 = State()
    comparison_result = State()

    # Додаткові функції
    filter_heroes = State()
    sort_heroes = State()
