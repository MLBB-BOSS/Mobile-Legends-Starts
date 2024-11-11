# main.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from core.info_handler import start, get_main_menu
from services.database import init_db, get_db

def main():
    init_db()  # Ініціалізуємо базу даних

    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    # Додавання обробників команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", get_main_menu))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
