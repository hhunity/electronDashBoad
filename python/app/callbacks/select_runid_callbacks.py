import dash  # Dash本体。Flask + React + Plotly をまとめたフレームワーク
from dash import callback, Output, Input, html, MATCH, State,dependencies,callback_context
import dash_bootstrap_components as dbc
import os
import json
import datetime
import components.graph as graph
import callbacks.get_runid_callbacks as get_runid

@callback(
    Output({"type":"selected-run-id", "prefix": MATCH}, "data"),
    Input({"type": "runid-item","prefix": MATCH, "runid": dash.dependencies.ALL}, "n_clicks"),
    Input({"type":"selected-file-version","prefix":MATCH}, "data"),
    State({"type":"selected-run-id","prefix":MATCH}, "data"),
    State({"type":"selected-file","prefix":MATCH}, "data"),
    prevent_initial_call=True,
)
def select_run_id(n_clicks,_version,current_selected, selected_file):#, _version, current_selected, selected_file
    """
    run_id をクリックしたら選択/解除。自動更新でファイルが変わった場合、最新の run_id に自動で切り替え。
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    # ユーザークリックか自動更新かを判断
    triggered_id = ctx.triggered_id

    # ユーティリティ: ファイルから run_end の時刻と行番号を辞書で返す
    def load_run_times(path):
        info = {}
        if not path or not os.path.isfile(path):
            return info
        try:
            with open(path, "r") as f:
                for idx, line in enumerate(f):
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if obj.get("type") == "run_end" and "run_id" in obj:
                        rid = obj.get("run_id")
                        t_val = get_runid.parse_time(obj.get("time"))
                        prev = info.get(rid)
                        if (
                            prev is None
                            or (t_val is not None and (prev["time"] is None or t_val > prev["time"]))
                            or (t_val == (prev["time"] or None) and idx > prev["order"])
                        ):
                            info[rid] = {"time": t_val, "order": idx}
        except Exception:
            return info
        return info

    run_times = load_run_times(selected_file)

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
            return dash.no_update # 無クリック(初期値)は無視
        if clicked_rid == current_selected:
            return None  # トグル解除
        return clicked_rid

    # 自動更新（selected-file-version）の場合
    if not run_times:
        return dash.no_update

    # 現在選択の時刻/行番号
    current_entry = run_times.get(current_selected) or {}
    current_time = current_entry.get("time")
    current_order = current_entry.get("order", -1)

    # 最新の run_id を探す（time 最大）
    latest_rid = None
    latest_time = None
    latest_order = -1
    for rid, info in run_times.items():
        t = info.get("time")
        order = info.get("order", -1)
        if latest_rid is None:
            latest_rid = rid
            latest_time = t
            latest_order = order
            continue
        if (
            (latest_time is None and t is not None)
            or (t is not None and latest_time is not None and t > latest_time)
            or (t == latest_time and order > latest_order)
        ):
            latest_rid = rid
            latest_time = t
            latest_order = order

    # 新しい run_id が増えた/より新しい場合のみ切り替え
    if latest_rid and (
        current_selected is None
        or current_time is None
        or (
            latest_time is not None
            and (
                latest_time > current_time
                or (latest_time == current_time and latest_order > current_order)
            )
        )
    ):
        return latest_rid

    return dash.no_update

# @app.callback(
#     Output("selected-run-id", "data"),
#     Output("selected-run-id-time", "data"),
#     Input({"type": "runid-item", "runid": dash.dependencies.ALL}, "n_clicks"),
#     Input("selected-file-version", "data"),
#     State("selected-run-id", "data"),
#     State("selected-file", "data"),
#     prevent_initial_call=True,
# )
# def select_run_id(n_clicks, _version, current_selected, selected_file):
#     """
#     run_id をクリックしたら選択/解除。自動更新でファイルが変わった場合、最新の run_id に自動で切り替え。
#     """
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return dash.no_update, dash.no_update

#     # ユーザークリックか自動更新かを判断
#     triggered_id = ctx.triggered_id

#     # ユーティリティ: ファイルから run_end 時刻を辞書で返す
#     def load_run_times(path):
#         times = {}
#         if not path or not os.path.isfile(path):
#             return times
#         try:
#             with open(path, "r") as f:
#                 for line in f:
#                     try:
#                         obj = json.loads(line)
#                     except Exception:
#                         continue
#                     if obj.get("type") == "run_end" and "run_id" in obj:
#                         rid = obj.get("run_id")
#                         t_val = parse_time(obj.get("time"))
#                         prev = times.get(rid)
#                         if prev is None or (t_val is not None and (prev is None or t_val > prev)):
#                             times[rid] = t_val
#         except Exception:
#             return times
#         return times

#     run_times = load_run_times(selected_file)

#     # クリック時の処理
#     clicked_rid = None
#     triggered_value = ctx.triggered[0].get("value") if ctx.triggered else None
#     if isinstance(triggered_id, dict):
#         clicked_rid = triggered_id.get("runid")
#     elif isinstance(triggered_id, str):
#         try:
#             parsed = json.loads(triggered_id)
#             if isinstance(parsed, dict):
#                 clicked_rid = parsed.get("runid")
#         except Exception:
#             clicked_rid = None

#     if clicked_rid:
#         if not triggered_value:
#             return dash.no_update, dash.no_update  # 無クリック(初期値)は無視
#         if clicked_rid == current_selected:
#             return None, None  # トグル解除
#         return clicked_rid, run_times.get(clicked_rid)

#     # 自動更新（selected-file-version）の場合
#     if not run_times:
#         return dash.no_update, dash.no_update

#     # 現在選択の時刻
#     current_time = run_times.get(current_selected)

#     # 最新の run_id を探す（time 最大）
#     latest_rid = None
#     latest_time = None
#     for rid, t in run_times.items():
#         if latest_time is None or (t is not None and (latest_time is None or t > latest_time)):
#             latest_rid = rid
#             latest_time = t

#     # 新しい run_id が増えた/より新しい場合のみ切り替え
#     if latest_rid and (current_selected is None or current_time is None or (latest_time is not None and latest_time > current_time)):
#         return latest_rid, latest_time

#     return dash.no_update, dash.no_update

@callback(
    Output({"type": "detail-graph", "prefix": MATCH}, "figure"),
    Input({"type": "file-raw", "prefix": MATCH}, "data"),
    Input({"type": "selected-run-id", "prefix": MATCH}, "data"),
)
def update_graph(raw_lines, run_id):
    if not raw_lines:
        return graph.build_fig()

    xs = []
    ys = []

    for line in raw_lines:
        try:
            obj = json.loads(line)
        except:
            continue

        if run_id is None or obj.get("run_id") == run_id:
            if "frame_id" in obj and "elapsed_ms" in obj:
                xs.append(obj["frame_id"])
                ys.append(obj["elapsed_ms"])

    return graph.build_fig(xs, ys)
