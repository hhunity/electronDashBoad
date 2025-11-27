from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

def build_fig(xs=None, ys=None, title=None):
    """Build a scatter-only figure with consistent dark styling."""
    fig = go.Figure()
    fig.update_layout(
        height=300,
        margin=dict(l=5, r=5, t=5, b=5),
        title=title or None,
        #template="ggplot2",#plotly_dark
        #paper_bgcolor="#1a1a1a",#グラフ全体（外側の紙）の背景色。
        #plot_bgcolor="#111",#プロット内の色
        xaxis_title="line",
        yaxis_title="d Y",
    )
    if xs and ys:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", name="elapsed_ms"))
    return fig

def make_graph(id_prefix):
    return  dcc.Graph(id={"type": "detail-graph", "prefix": id_prefix},
                    style={"height": "340px", "margin": "0"},
                    figure=build_fig())



