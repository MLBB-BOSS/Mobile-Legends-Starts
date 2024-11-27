# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MenuButton(Enum):
    NAVIGATION = "🧭 Navigation"
    PROFILE = "🪪 My Profile"
    HEROES = "🥷 Heroes"
    GUIDES = "📖 Guides"
    SEARCH_HERO = "🔎 Search Hero"
    FIGHTER = "🗡️ Fighter"
    TANK = "🛡️ Tank"
    MAGE = "🧙‍♂️ Mage"
    MARKSMAN = "🏹 Marksman"
    ASSASSIN = "⚔️ Assassin"
    SUPPORT = "🧬 Support"
    COMPARISON = "⚖️ Comparison"
    BACK = "🔄 Back"
    NEW_GUIDES = "🆕 New Guides"
    POPULAR_GUIDES = "🌟 Popular Guides"
    BEGINNER_GUIDES = "📘 For Beginners"
    ADVANCED_TECHNIQUES = "🧙 Advanced Techniques"
    TEAMPLAY_GUIDES = "🛡️ Teamplay Guides"
    COUNTER_PICKS = "⚖️ Counter Picks"
    COUNTER_SEARCH = "🔎 Counter Pick Search"
    COUNTER_LIST = "📝 Hero List"
    CREATE_BUILD = "🏗️ Create Build"
    MY_BUILDS = "📄 My Builds"
    POPULAR_BUILDS = "💎 Popular Builds"
    BUILDS = "⚜️ Builds"
    CURRENT_VOTES = "📍 Current Polls"
    MY_VOTES = "📋 My Votes"
    SUGGEST_TOPIC = "➕ Suggest Topic"
    VOTING = "📊 Voting"
    ACTIVITY = "📊 Overall Activity"
    RANKING = "🥇 Ranking"
    GAME_STATS = "🎮 Game Statistics"

heroes_by_class = {
    "Fighter": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyrroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fredrinn", "Arlott", "Leomord", "Thamuz", "Badang", "Guinevere"
    ],
    # Add other hero classes...
}

menu_button_to_class = {
    MenuButton.TANK.value: "Tank",
    MenuButton.MAGE.value: "Mage",
    MenuButton.MARKSMAN.value: "Marksman",
    MenuButton.ASSASSIN.value: "Assassin",
    MenuButton.SUPPORT.value: "Support",
    MenuButton.FIGHTER.value: "Fighter",
}

def create_menu(buttons, row_width=2):
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("All items in buttons must be instances of MenuButton or str.")
    keyboard = [
        [KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_heroes_menu():
    return create_menu(
        [
            MenuButton.FIGHTER,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.COMPARISON,
            MenuButton.BACK,
            MenuButton.SEARCH_HERO
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    row_width = 3
    keyboard = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    keyboard.append([KeyboardButton(text=MenuButton.BACK.value)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=1
    )

def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_profile_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        row_width=2
    )
