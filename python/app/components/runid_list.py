from dash import html, dcc
import dash_bootstrap_components as dbc
import components.toggle_button as toggle

def make_runcode_list(id_prefix):
    return  html.Div(
            id=f"{id_prefix}-sidebar-content",
            children=[
                dcc.Interval(id={"type":"auto-refresh-interval","prefix":id_prefix}, interval=2000, disabled=True),
                dcc.Store(id={"type":"selected-file-version","prefix":id_prefix}, data={"version": 0, "mtime": None}),

                html.Div([
                    dbc.Label("log Path", html_for=f"{id_prefix}-path"),
                    dbc.Input(type="email", id={"type": "log-path","prefix": id_prefix}, placeholder="Enter og Path",value="./python/logs"),
                ]),
                html.Div([
                    # .jsonl ファイルの一覧（mtime 降順）
                    dbc.Label("file list", html_for=f"{id_prefix}-filelist"),
                    # html.Div 内で動的に子要素を差し替える。子要素には id={"type":"jsonl-item",...} のDivを入れる。
                    dbc.ListGroup(id={"type":"file-list", "prefix": id_prefix}),
                ]),
                html.Div([
                    # run_end から抽出した run_id 一覧（time 新しい順）
                    dbc.Label("run id list", html_for=f"{id_prefix}-runidlist"),
                    dbc.ListGroup(id={"type":"runid-list", "prefix": id_prefix}),
                ]),
                dbc.Col(
                        toggle.make_toggle_butoon(id_prefix),className="d-flex justify-content-start"),
            ],
            )
