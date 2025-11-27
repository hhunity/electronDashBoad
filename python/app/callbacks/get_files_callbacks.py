from dash import callback, Output, Input, html, MATCH, State
import dash
import dash_bootstrap_components as dbc
import os

@callback(
    Output({"type": "file-list", "prefix": MATCH}, "children"),
    Input({"type": "log-path","prefix": MATCH}, "value"),
    Input({"type": "selected-file", "prefix": MATCH}, "data"),
    prevent_initial_call=False,
)
def show_files(path,selected_path): #selected_path
    """
    ログパスの .jsonl を mtime 新しい順に並べ、クリック可能なリストで返す。
    Dashのコールバックは「Outputをどう埋めるか」を定義する関数。
    Input/Stateの値が変わるとこの関数が呼ばれ、返り値がOutputに反映される。
    """

    if not path:
        return "パスを入力するとファイル一覧を表示します。"
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        return f"存在しないパスです: {abs_path}"
    if not os.path.isdir(abs_path):
        return f"ディレクトリを指定してください: {abs_path}"
    
    try:
        candidates = [e for e in os.listdir(abs_path) if e.endswith(".jsonl")]
        entries = sorted(
            candidates,
            key=lambda name: os.path.getmtime(os.path.join(abs_path, name)),
            reverse=True,
        )
    except Exception as e:
        return f"読み取りに失敗しました: {e}"

    if not entries:
        return f"jsonlファイルがありません: {abs_path}"

    ctx = dash.callback_context
    prefix = None
    if ctx.triggered_id and isinstance(ctx.triggered_id, dict):
        prefix = ctx.triggered_id.get("prefix")
    if prefix is None:
        # fallback: pick prefix from first input if available
        for item in getattr(ctx, "inputs_list", []):
            if isinstance(item.get("id"), dict):
                prefix = item["id"].get("prefix")
                if prefix is not None:
                    break
    
    return [
        dbc.ListGroupItem(
            e,
            id={"type": "jsonl-item","prefix": prefix,"path": os.path.join(abs_path, e)},
            n_clicks=0,
            action=True,
            active=True if os.path.join(abs_path, e) == selected_path else False
        )
        for e in entries
    ]