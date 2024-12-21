import io
import matplotlib.pyplot as plt

def create_chart(data: list[int], title: str = "Default Title") -> io.BytesIO:
    """
    Створює простий графік на основі переданих даних.
    """
    plt.figure(figsize=(4, 4))
    plt.plot(data, marker='o', linestyle='-', color='blue')
    plt.title(title)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close()
    return buf