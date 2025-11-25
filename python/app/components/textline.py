from dash import html, dcc
import dash_bootstrap_components as dbc

def make_textline(id_prefix):
    return dcc.Textarea(
                            id=f"{id_prefix}-textline",
                            style={
                                "width": "100%",
                                "height": "100%",
                                "resize": "none",          # ← この1行でドラッグ禁止
                                # "whiteSpace": "pre",
                                # "backgroundColor": "#111",
                                # "color": "#eee",
                                # "border": "1px solid #333",
                            },
                            readOnly=True,
                        )



                        