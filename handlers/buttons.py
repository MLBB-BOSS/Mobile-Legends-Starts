import logging
from aiogram import types, Dispatcher
from keyboards.menus import MenuButton, get_main_menu, get_navigation_menu, get_heroes_menu

logger = logging.getLogger("handlers.buttons")

# Обробка стартового повідомлення (Натискання кнопки "Start")
async def cmd_start(message: types.Message):
    logger.info(f"Новий користувач: {message.from_user.username} з ID: {message.from_user.id}")
    await message.answer(
        "Привіт! Я твій асистент по грі Mobile Legends. Вибери опцію з меню.",
        reply_markup=get_main_menu()
    )

# Обробка натискання кнопки головного меню
async def handle_main_menu_buttons(message: types.Message):
    user_choice = message.text

    if user_choice == MenuButton.NAVIGATION.value:
        # Показуємо меню навігації
        await message.answer("Оберіть опцію навігації:", reply_markup=get_navigation_menu())
    
    elif user_choice == MenuButton.PROFILE.value:
        # Показуємо меню профілю
        await message.answer("Оберіть опцію профілю:", reply_markup=get_heroes_menu())
    
    else:
        await message.answer("Невідома команда, спробуйте ще раз", reply_markup=get_main_menu())

# Обробка натискання кнопок в меню навігації
async def handle_navigation_buttons(message: types.Message):
    user_choice = message.text

    if user_choice == MenuButton.HEROES.value:
        # Показуємо меню героїв
        await message.answer("Оберіть клас героя:", reply_markup=get_heroes_menu())
    
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до головного меню
        await message.answer("Повертаємось до головного меню", reply_markup=get_main_menu())

    else:
        await message.answer("Невідома команда в меню навігації. Спробуйте ще раз.", reply_markup=get_navigation_menu())

# Обробка кнопок героїв
async def handle_heroes_buttons(message: types.Message):
    user_choice = message.text

    if user_choice in [MenuButton.TANK.value, MenuButton.MAGE.value, MenuButton.MARKSMAN.value,
                       MenuButton.ASSASSIN.value, MenuButton.SUPPORT.value, MenuButton.FIGHTER.value]:
        # Тут можна обробляти вибір конкретного героя
        await message.answer(f"Вибрано клас героя: {user_choice}. Тепер перегляньте список героїв.", reply_markup=get_heroes_menu())
    
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось назад до меню навігації
        await message.answer("Повертаємось до меню навігації.", reply_markup=get_navigation_menu())
    
    else:
        await message.answer("Невідома команда в меню героїв. Спробуйте ще раз.", reply_markup=get_heroes_menu())

# Реєстрація обробників у Dispatcher
def register_buttons_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, commands=["start"])
    dp.message.register(handle_main_menu_buttons, lambda message: message.text in [MenuButton.NAVIGATION.value, MenuButton.PROFILE.value])
    dp.message.register(handle_navigation_buttons, lambda message: message.text in [MenuButton.HEROES.value, MenuButton.BACK.value])
    dp.message.register(handle_heroes_buttons, lambda message: message.text in [
        MenuButton.TANK.value, MenuButton.MAGE.value, MenuButton.MARKSMAN.value, MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value, MenuButton.FIGHTER.value, MenuButton.BACK.value
    ])
