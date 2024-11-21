# File: handlers/menu_handlers.py

@router.message(F.text == loc.get_message("buttons.counter_picks"))
async def show_counter_picks_menu(message: Message):
    logger.info(f"Користувач {message.from_user.id} відкрив меню контр-піків")
    try:
        await message.answer(
            loc.get_message("messages.counter_picks_menu"),
            reply_markup=NavigationMenu().get_counter_picks_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка при відображенні меню контр-піків: {e}")
        await message.answer(
            loc.get_message("errors.general"),
            reply_markup=NavigationMenu().get_main_navigation()
        )
