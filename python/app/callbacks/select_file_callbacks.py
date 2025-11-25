import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import callback, Output, Input, html, MATCH, State,dependencies,callback_context
import dash_bootstrap_components as dbc
import os
import json
import datetime

@callback(
    Output({"type":"selected-file", "prefix": MATCH}, "data"),
    Input({"type":"jsonl-item","prefix": MATCH, "path": dependencies.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def show_file_content(n_clicks):
    """
    ファイルクリック or run_id 変更で発火。
    - ファイルを選択したら内容を表示し、selected-file を更新。
    - run_id が選択されていれば、その run_id の行だけを表示し、同じデータでグラフ描画。
    DashのInput/Outputは宣言的: Outputで指定したコンポーネント属性を、この関数の返り値で置き換える。
    Stateは「監視はしないが現在値を読みたい」入力。
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    trig = ctx.triggered_id
    triggered_by_run = trig == "selected-run-id"

    path = None
    new_selected = dash.no_update

    # ファイルクリック時
    if not n_clicks or all((c is None or c == 0) for c in n_clicks):
        return dash.no_update
    if isinstance(trig, dict):
        path = trig.get("path")
    else:
        try:
            path = json.loads(ctx.triggered[0]["prop_id"].split(".")[0]).get("path")
        except Exception:
            return dash.no_update
    new_selected = path

    if not path or not os.path.isfile(path):
        return dash.no_update

    return new_selected