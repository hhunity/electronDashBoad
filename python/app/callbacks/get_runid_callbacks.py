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
    # Input("selected-file-version", "data"),
)
def update_runid_list(selected_path,selected_run_id):
    """選択中ファイルの run_end から run_id を抽出し、time 新しい順で表示。_version は監視用ダミー。"""
    if not selected_path or not os.path.isfile(selected_path):
        return ""

    run_times = {}
    try:
        with open(selected_path, "r") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") == "run_end" and "run_id" in obj:
                    rid = obj.get("run_id")
                    t_val = parse_time(obj.get("time"))
                    prev = run_times.get(rid)
                    if prev is None or (t_val is not None and (prev is None or t_val > prev)):
                        run_times[rid] = t_val
    except Exception as e:
        return f"run_id抽出に失敗しました: {e}"

    if not run_times:
        return "run_end の run_id が見つかりません。"

    # sort by time desc (None is treated as oldest)
    sorted_run_ids = [
        rid for rid, _ in sorted(
            run_times.items(),
            key=lambda kv: kv[1] if kv[1] is not None else float("-inf"),
            reverse=True,
        )
    ]
    
    ctx = dash.callback_context
    prefix = None
    for item in getattr(ctx, "inputs_list", []):
        if isinstance(item.get("id"), dict) and "prefix" in item["id"]:
            prefix = item["id"]["prefix"]
            break
    # if ctx.triggered_id and isinstance(ctx.triggered_id, dict):
    #     prefix = ctx.triggered_id.get("prefix")
    # if prefix is None:
    #     # fallback: pick prefix from first input if available
    #     for item in getattr(ctx, "inputs_list", []):
    #         if isinstance(item.get("id"), dict):
    #             prefix = item["id"].get("prefix")
    #             if prefix is not None:
    #                 break

    return [
        # html.Div(
        #     rid,
        #     id={"type": "runid-item", "runid": rid},
        #     n_clicks=0,
        #     style={
        #         "padding": "6px",
        #         "border": "1px solid #333",
        #         "marginBottom": "4px",
        #         "cursor": "pointer",
        #         "borderRadius": "4px",
        #         # "backgroundColor": "#2f6eff" if rid == selected_run_id else "#181818",
        #         # "color": "#fff" if rid == selected_run_id else "#eee",
        #     },
        # )
        # for rid in sorted_run_ids

        dbc.ListGroupItem(
            rid,
            id={"type": "runid-item","prefix": prefix,"runid": rid},
            n_clicks=0,
            action=True,
            active=True if rid == selected_run_id else False
        )
        for rid in sorted_run_ids
    ]