import os
import json
import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import html, dcc, Input, Output, State  # html: HTMLタグ, dcc: Dash Core Components, Input/Output/State: コールバックの入出力宣言
import plotly.graph_objs as go
from datetime import datetime
import dash_bootstrap_components as dbc
import components.sidebar as sidebar
import components.contents as contents

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

from callbacks import get_files_callbacks
from callbacks import get_runid_callbacks
from callbacks import select_file_callbacks
from callbacks import select_runid_callbacks

content = html.Div(
    [
        # dbc.Row([
            contents.make_contents("1"),
            contents.make_contents("2")
    # ])
    ]
    )

sideber = html.Div(
    [
        sidebar.make_sidebar()
    ]
    )

# ---- その後に layout を定義 ----
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sideber, width="auto", className='bg-light'),
                dbc.Col(content, width=True),
                ],
            style={"height": "100vh"},
            ),
        ],
    className='bg-light g-0',
    fluid=True,
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=True)
