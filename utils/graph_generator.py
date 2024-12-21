# utils/graph_generator.py

import networkx as nx
import plotly.graph_objects as go
import io

def create_network_graph():
    # Створення графа
    G = nx.Graph()
    G.add_edges_from([
        ("Hero A", "Hero B"),
        ("Hero A", "Hero C"),
        ("Hero B", "Hero D"),
        ("Hero C", "Hero D"),
        ("Hero D", "Hero E"),
    ])

    # Створення позицій вершин
    pos = nx.spring_layout(G)

    # Створення Plotly графіка
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='#1f78b4',
            size=10,
            line_width=2
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Взаємозв\'язки Героїв',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper")],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Збереження графіка у байтовий буфер
    img_bytes = fig.to_image(format="png")
    return img_bytes
