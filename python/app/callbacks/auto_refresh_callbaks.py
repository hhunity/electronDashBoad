
from dash import callback, Output, Input, html, MATCH, State
import dash
import dash_bootstrap_components as dbc
import os


@callback(
    Output({"type":"toggle_button", "prefix": MATCH}, "label"),
    Output({"type":"auto-refresh-interval","prefix":MATCH}, "disabled"),
    Input({"type":"toggle_button", "prefix": MATCH}, "value"),
)
def toggle_auto_refresh(switch_checked):
    """自動更新ボタンの ON/OFF 表示と Interval の有効/無効を切り替え。"""
    on = bool(switch_checked == 1)
    label = "Auto Refresh ON" if on else "Auto Refresh OFF"
    # Interval は disabled=False で動くため、ON なら disabled を False にする
    return label, (not on)

@callback(
    Output({"type":"selected-file-version","prefix":MATCH}, "data"),
    Input({"type":"auto-refresh-interval","prefix":MATCH},"n_intervals"),
    State({"type": "selected-file", "prefix": MATCH}, "data"),
    State({"type":"selected-file-version","prefix":MATCH}, "data"),
)
def refresh_selected_file_version(_, selected_file, current):
    """
    自動更新が ON のときだけ走る。
    選択ファイルの mtime が変わったら version をインクリメントし、run_id リストを更新させる。
    """
    if not selected_file or not os.path.isfile(selected_file):
        return dash.no_update

    try:
        mtime = os.path.getmtime(selected_file)
    except OSError:
        return dash.no_update

    current = current or {"version": 0, "mtime": None}
    if current.get("mtime") == mtime:
        return dash.no_update

    return {"version": current.get("version", 0) + 1, "mtime": mtime}
