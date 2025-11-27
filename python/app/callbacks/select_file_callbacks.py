import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import callback, Output, Input, html, MATCH, State,dependencies,callback_context
import dash_bootstrap_components as dbc
import os
import json
import datetime

# --- A: ファイルだけ選択（path 保存だけ） ---
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
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    trig = ctx.triggered_id  # {"type":..., "prefix":..., "path":...}
    return trig["path"]

# --- B: Pathを元にファイルを読んでStoreに保存 ---
@callback(
    Output({"type": "file-raw", "prefix": MATCH}, "data"),
    Input({"type": "selected-file", "prefix": MATCH}, "data"),
)
def load_raw_file(path):
    if not path or not os.path.isfile(path):
        return None

    try:
        with open(path, "r") as f:
            return f.readlines()
    except:
        return None
    
# --- C: ファイルと選択されたrun idをもとに中身を表示する ---
@callback(
    Output({"type": "textline", "prefix": MATCH}, "value"),
    Input({"type": "file-raw", "prefix": MATCH}, "data"),
    Input({"type": "selected-run-id", "prefix": MATCH}, "data"),
)
def update_file_content(raw_lines, run_id):
    if not raw_lines:
        return ""

    if not run_id:
        return "".join(raw_lines)

    filtered = []
    for line in raw_lines:
        try:
            obj = json.loads(line)
        except:
            continue
        if obj.get("run_id") == run_id:
            filtered.append(line.rstrip("\n"))

    return "\n".join(filtered) if filtered else "(該当なし)"

# --- B: ファイル内容を読む専用 ---

    
