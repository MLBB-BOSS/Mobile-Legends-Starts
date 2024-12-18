# utils/helpers.py

from datetime import datetime
from texts import (
    PROFILE_INTERACTIVE_TEXT,
    STATISTICS_INTERACTIVE_TEXT,
    ACHIEVEMENTS_INTERACTIVE_TEXT
)


def generate_profile_message(profile_data):
    """
    Генерує форматоване повідомлення профілю користувача.

    :param profile_data: Словник з даними профілю користувача.
    :return: Форматоване повідомлення профілю у форматі HTML.
    """
    last_update = profile_data.get('last_update')
    if isinstance(last_update, datetime):
        last_update_formatted = last_update.strftime('%d.%m.%Y %H:%M')
    else:
        last_update_formatted = 'N/A'

    return PROFILE_INTERACTIVE_TEXT.format(
        username=profile_data.get('username', 'N/A'),
        level=profile_data.get('level', 'N/A'),
        rating=profile_data.get('rating', 'N/A'),
        achievements_count=profile_data.get('achievements_count', 0),
        screenshots_count=profile_data.get('screenshots_count', 0),
        missions_count=profile_data.get('missions_count', 0),
        quizzes_count=profile_data.get('quizzes_count', 0),
        total_matches=profile_data.get('total_matches', 0),
        total_wins=profile_data.get('total_wins', 0),
        total_losses=profile_data.get('total_losses', 0),
        tournament_participations=profile_data.get('tournament_participations', 0),
        badges_count=profile_data.get('badges_count', 0),
        last_update=last_update_formatted
    )


def generate_statistics_message(statistics_data):
    """
    Генерує форматоване повідомлення статистики користувача.

    :param statistics_data: Словник з даними статистики користувача.
    :return: Форматоване повідомлення статистики у форматі HTML.
    """
    return STATISTICS_INTERACTIVE_TEXT.format(
        activity=statistics_data.get('activity', 'N/A'),
        ranking=statistics_data.get('ranking', 'N/A'),
        game_stats=statistics_data.get('game_stats', 'N/A'),
    )


def generate_achievements_message(achievements_data):
    """
    Генерує форматоване повідомлення досягнень користувача.

    :param achievements_data: Словник з даними досягнень користувача.
    :return: Форматоване повідомлення досягнень у форматі HTML.
    """
    return ACHIEVEMENTS_INTERACTIVE_TEXT.format(
        badges=achievements_data.get('badges', 0),
        progress=achievements_data.get('progress', 'N/A'),
        tournament_stats=achievements_data.get('tournament_stats', 'N/A'),
        awards=achievements_data.get('awards', 'N/A')
    )