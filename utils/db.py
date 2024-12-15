import sqlite3

def get_user_profile(user_id):
    """
    Отримує дані профілю користувача з бази даних.
    :param user_id: Telegram ID користувача.
    :return: Словник з даними користувача.
    """
    connection = sqlite3.connect("database.db")  # Підключення до бази даних
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, rating, matches, wins, losses
        FROM users
        WHERE telegram_id = ?
    """, (user_id,))
    
    result = cursor.fetchone()
    connection.close()

    if result:
        return {
            "username": result[0],
            "rating": result[1],
            "matches": result[2],
            "wins": result[3],
            "losses": result[4],
            "sessions": [1, 2, 3, 4, 5],  # Приклад даних для графіку
            "ratings": [100, 120, 150, 180, 210]
        }
    else:
        return {
            "username": "unknown",
            "rating": 0,
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "sessions": [0],
            "ratings": [0]
        }
