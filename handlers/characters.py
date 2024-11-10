# handlers/characters.py
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from utils.data_loader import load_hero_data

async def get_hero_description(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Будь ласка, введіть назву героя. Приклад: /description Alucard")
        return
    hero_name = ' '.join(context.args).title()
    hero_class = get_hero_class(hero_name)
    if hero_class == "Unknown":
        await update.message.reply_text("Герой не знайдений.")
        return
    description = load_hero_data(hero_class, hero_name, "description")
    if description:
        await update.message.reply_text(description.get("lore", "Опис не знайдений."))
    else:
        await update.message.reply_text("Опис не знайдений.")

def get_hero_class(hero_name):
    for hero_class, heroes in heroes_structure.items():
        if hero_name in heroes:
            return hero_class
    return "Unknown"

router = CommandHandler('description', get_hero_description)# Інформація про персонажів
