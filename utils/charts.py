import matplotlib.pyplot as plt
import io

def generate_activity_chart(user_data):
    """
    Генерує графік активності користувача.
    :param user_data: Словник з даними користувача (sessions, ratings).
    :return: BytesIO зображення графіку.
    """
    sessions = user_data['sessions']
    ratings = user_data['ratings']

    plt.figure(figsize=(6, 4))
    plt.plot(sessions, ratings, marker='o', linestyle='-', linewidth=2)
    plt.title('Графік зміни рейтингу')
    plt.xlabel('Сеанс')
    plt.ylabel('Рейтинг')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
