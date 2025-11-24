import os
import json
import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import html, dcc, Input, Output, State  # html: HTMLタグ, dcc: Dash Core Components, Input/Output/State: コールバックの入出力宣言
import plotly.graph_objs as go
from datetime import datetime
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

sidebar = html.Div(
    [
        dbc.Row(
            [
                html.P('Settings')
                ],
            style={"height": "5vh"}, className='bg-primary text-white'
            ),
        dbc.Row(
            [
                html.P('Categorical and Continuous Variables')
                ],
            style={"height": "50vh"}, className='bg-secondary text-white'
            ),
        dbc.Row(
            [
                html.P('Target Variables')
                ],
            style={"height": "45vh"}, className='bg-dark text-white'
            )
    ],
)

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Distribution of Categorical Variable'),
                        ],
                    className='bg-white'
                    ),
                dbc.Col(
                    [
                        html.P('Distribution of Continuous Variable')
                    ],
                    className='bg-dark text-white'
                    )
            ],
            style={"height": "50vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Correlation Matrix Heatmap')
                    ],
                    className='bg-light'
                    )
            ],
            style={"height": "50vh"}
            )
        ]
    )

# ---- その後に layout を定義 ----
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ],
            style={"height": "100vh"}
            ),
        ],
    fluid=True
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=False)
