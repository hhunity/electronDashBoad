from dash import html, dcc
import dash_bootstrap_components as dbc

def make_textline(id_prefix):
    return html.Div(
        [
            dcc.Store(id={"type": "file-raw", "prefix": id_prefix}),
            dcc.Textarea(
                            id={"type":"textline", "prefix": id_prefix},
                            style={
                                "width": "100%",
                                "height": "100%",
                                "resize": "none",          # ← この1行でドラッグ禁止
                                "whiteSpace": "pre",
                                "overflowX": "auto",    # ← 横スクロールバーを表示
                                "overflowY": "auto",    # ← 縦スクロールも維持
                                # "backgroundColor": "#111",
                                # "color": "#eee",
                                # "border": "1px solid #333",
                            },
                            readOnly=True,
                        )
        ],
        style={"height": "100%"},
        )



                        