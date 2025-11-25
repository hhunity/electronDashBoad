from dash import html, dcc
import dash_bootstrap_components as dbc

def make_sidebar():
    return html.Div(
        [
            html.Button("≡", id="toggle-sidebar"),
        ],
        className='bg-light',
        id="sidebar"
    )