import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import callback, Output, Input, html, MATCH, State,dependencies,callback_context
import dash_bootstrap_components as dbc
import os
import json
import datetime

@callback(
    Output({"type":"selected-run-id", "prefix": MATCH}, "data"),
    Input({"type": "runid-item","prefix": MATCH, "runid": dash.dependencies.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def select_run_id(n_clicks):#, _version, current_selected, selected_file
    """
    run_id をクリックしたら選択/解除。自動更新でファイルが変わった場合、最新の run_id に自動で切り替え。
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    # ユーザークリックか自動更新かを判断
    triggered_id = ctx.triggered_id
    
    # クリック時の処理
    clicked_rid = None
    triggered_value = ctx.triggered[0].get("value") if ctx.triggered else None
    if isinstance(triggered_id, dict):
        clicked_rid = triggered_id.get("runid")
    elif isinstance(triggered_id, str):
        try:
            parsed = json.loads(triggered_id)
            if isinstance(parsed, dict):
                clicked_rid = parsed.get("runid")
        except Exception:
            clicked_rid = None

    if clicked_rid:
        if not triggered_value:
            return dash.no_update, dash.no_update  # 無クリック(初期値)は無視
        # if clicked_rid == current_selected:
        #     return None, None  # トグル解除
        return clicked_rid
