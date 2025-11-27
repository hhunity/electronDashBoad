from dash import html, dcc
import dash_bootstrap_components as dbc

def make_toggle_butoon(id_prefix):
    return  dbc.Switch(
                    id={"type":"toggle_button", "prefix": id_prefix},
                    label="auto",
                    value=False,
                )



                        