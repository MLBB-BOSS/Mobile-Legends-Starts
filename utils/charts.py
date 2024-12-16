import plotly.graph_objects as go
from io import BytesIO

def generate_rating_chart(
    rating_history,
    title="Ігрова статистика рейтингу",
    line_color='#00FFEA',
    marker_color='#FF5733',
    marker_border_color='#FFD700',
    width=800,
    height=600
):
    """
    Генерує графік рейтингу користувача.

    :param rating_history: List[int] - Історія рейтингу користувача.
    :param title: str - Заголовок графіку (за замовчуванням "Ігрова статистика рейтингу").
    :param line_color: str - Колір лінії графіку (за замовчуванням '#00FFEA').
    :param marker_color: str - Колір маркерів (за замовчуванням '#FF5733').
    :param marker_border_color: str - Колір обводки маркерів (за замовчуванням '#FFD700').
    :param width: int - Ширина графіку (за замовчуванням 800).
    :param height: int - Висота графіку (за замовчуванням 600).

    :return: BytesIO - Зображення графіка у байтовому форматі.
    """
    if not rating_history:
        raise ValueError("rating_history не може бути порожнім.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=rating_history,
        x=list(range(len(rating_history))),
        mode='lines+markers',
        line=dict(color=line_color, width=3),
        marker=dict(size=12, color=marker_color, line=dict(width=2, color=marker_border_color))
    ))

    fig.update_layout(
        title=title,
        title_font=dict(size=22, color='#FF5733'),
        xaxis=dict(title='Період', title_font=dict(size=14, color='#00FFEA')),
        yaxis=dict(title='Рейтинг', title_font=dict(size=14, color='#00FFEA')),
        template='plotly_dark',
        width=width,
        height=height
    )

    # Створення зображення у форматі BytesIO
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png', engine='kaleido')
    img_bytes.seek(0)

    return img_bytes
