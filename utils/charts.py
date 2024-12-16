import plotly.graph_objects as go
from io import BytesIO

def generate_rating_chart(rating_history):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=rating_history,
        x=list(range(len(rating_history))),
        mode='lines+markers',
        line=dict(color='#00FFEA', width=3),
        marker=dict(size=12, color='#FF5733', line=dict(width=2, color='#FFD700'))
    ))

    fig.update_layout(
        title="Ігрова статистика рейтингу",
        title_font=dict(size=22, color='#FF5733'),
        xaxis=dict(title='Період', title_font=dict(size=14, color='#00FFEA')),
        yaxis=dict(title='Рейтинг', title_font=dict(size=14, color='#00FFEA')),
        template='plotly_dark'
    )

    # Збереження у BytesIO
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)
    return img_bytes
