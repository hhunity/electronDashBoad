from dash import callback, Output, Input, html,MATCH
import dash_bootstrap_components as dbc
import dash
import os
import json
import datetime

def parse_time(value):
    """Parse time field to a float timestamp (None on failure)."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value
        if "T" in s:
            try:
                return datetime.fromisoformat(s).timestamp()
            except ValueError:
                # truncate fractional seconds to 6 digits if longer
                try:
                    if "." in s:
                        base, frac = s.split(".", 1)
                        frac_digits = "".join(ch for ch in frac if ch.isdigit())
                        frac_adj = (frac_digits[:6]).ljust(6, "0")
                        return datetime.fromisoformat(f"{base}.{frac_adj}").timestamp()
                except Exception:
                    return None
            except Exception:
                return None
        try:
            return float(s)
        except Exception:
            return None
    return None

@callback(
    Output({"type":"runid-list", "prefix": MATCH}, "children"),
    Input({"type":"selected-file", "prefix": MATCH}, "data"),
    Input({"type":"selected-run-id", "prefix": MATCH}, "data"),
    Input({"type":"selected-file-version","prefix":MATCH}, "data"),
)
def update_runid_list(selected_path,selected_run_id,_version):
    """選択中ファイルの run_end から run_id を抽出し、time 新しい順で表示。_version は監視用ダミー。"""
    if not selected_path or not os.path.isfile(selected_path):
        return ""

    run_info = {}
    try:
        with open(selected_path, "r") as f:
            for idx, line in enumerate(f):
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") == "run_end" and "run_id" in obj:
                    rid = obj.get("run_id")
                    t_val = parse_time(obj.get("time"))
                    prev = run_info.get(rid)
                    # 新しい時刻、または同時刻なら後勝ち（ファイル後方＝新しいとみなす）
                    if (
                        prev is None
                        or (t_val is not None and (prev["time"] is None or t_val > prev["time"]))
                        or (t_val == (prev["time"] or None) and idx > prev["order"])
                    ):
                        run_info[rid] = {"time": t_val, "order": idx}
    except Exception as e:
        return f"run_id抽出に失敗しました: {e}"

    if not run_info:
        return "run_end の run_id が見つかりません。"

    # time が新しい順 (None は最後)、同時刻ならファイル後方を優先
    def sort_key(item):
        rid, info = item
        t = info["time"]
        order = info["order"]
        return (t is not None, t or float("-inf"), order)

    sorted_run_ids = [rid for rid, _ in sorted(run_info.items(), key=sort_key, reverse=True)]
    
    ctx = dash.callback_context
    prefix = None
    for item in getattr(ctx, "inputs_list", []):
        if isinstance(item.get("id"), dict) and "prefix" in item["id"]:
            prefix = item["id"]["prefix"]
            break
    return [
        dbc.ListGroupItem(
            rid,
            id={"type": "runid-item","prefix": prefix,"runid": rid},
            n_clicks=0,
            action=True,
            active=True if rid == selected_run_id else False
        )
        for rid in sorted_run_ids
    ]
