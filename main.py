# main.py

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from core import (
    get_main_menu,
    handle_screenshot,
    view_profile,
    view_leaderboard,
    handle_heroes_info,
    handle_help
)
from config.settings import TELEGRAM_BOT_TOKEN, ENABLE_QUIZZES, ENABLE_NEWS
from services.database import init_db

def main():
    # Ініціалізація бази даних
    init_db()
    
    # Створення Updater та Dispatcher
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Додавання обробника команди /start
    dispatcher.add_handler(CommandHandler('start', get_main_menu))

    # Додавання обробників для натискання кнопок меню
    dispatcher.add_handler(MessageHandler(Filters.regex('^Інформація про героїв$'), handle_heroes_info))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Завантажити скріншот$'), handle_screenshot))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Мій профіль$'), view_profile))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Лідерборд$'), view_leaderboard))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Допомога$'), handle_help))

    # Додавання інших обробників за потребою
    if ENABLE_QUIZZES:
        from handlers.quizzes import handle_quiz
        dispatcher.add_handler(CommandHandler('quiz', handle_quiz))

    if ENABLE_NEWS:
        from handlers.news import handle_news
        dispatcher.add_handler(CommandHandler('news', handle_news))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
