from dash import html, dcc
import dash_bootstrap_components as dbc
import components.graph as graph
import components.textline as textline
import components.runid_list as runcode

def make_contents(id_prefix):
    return html.Div(
        [
                dcc.Store(id={"type":"selected-file", "prefix": id_prefix}),
                dcc.Store(id={"type":"selected-run-id", "prefix": id_prefix}),

                dbc.NavbarSimple(
                    brand="NavbarSimple",
                    brand_href="#",
                    color="primary",
                    style={"padding": "0"},
                ),
                dbc.Row([
                    dbc.Col(
                        runcode.make_runcode_list(id_prefix),width=2),
                    dbc.Col(
                        graph.make_graph(id_prefix),width=5),
                    dbc.Col(
                        textline.make_textline(id_prefix),width=5),
                        ],
                    # className='bg-light',
                    className='g-0',
                ),
                
        ],
        className='bg-light',
        id=f"contents-{id_prefix}-files",
    )