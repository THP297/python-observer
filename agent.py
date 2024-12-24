from dash import html
import pandas as pd
from query_du_lieu import get_user_list
import time


# Dữ liệu mẫu cho "Danh sách agent"
status_colors = {
    "Available": "#4bc076",
    "Routing": "red",
    "Away": "#d7a416",
    "Lunch": "#f2cf5b",
    "Meeting": "#f36262",
    "Callback": "#b785cc",
    "Outbound": "#4da7e1",
    "Logout": "#ABB2B9",
    "Campaign": "#f2a6cf",
    "No ACD": "#f49756"
}

def render_agent_list(agent_data):
    #print("render_agent_list")
    if agent_data is None:
        agent_data = get_user_list()
    table_rows = [
        html.Tr([
            *[
                html.Td(
                    agent_data.iloc[i][col],
                    style={
                        "border": "1px solid #000",
                        "padding": "8px",
                        **({"backgroundColor": status_colors[agent_data.iloc[i]["Trạng thái"]], "color": "#fff"}
                           if col == "Trạng thái" and agent_data.iloc[i]["Trạng thái"] in status_colors else {})
                    }
                ) for col in agent_data.columns
            ]
        ], style={"border": "1px solid #000"})
        for i in range(len(agent_data))
    ]

    return html.Table([
        html.Thead(html.Tr([
            *[html.Th(col, style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}) for col in agent_data.columns]
        ], style={"border": "1px solid #000"})),
        html.Tbody(table_rows)
    ], id="agent-list",
        style={
        "width": "100%",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginBottom": "20px",
        "border": "1px solid #000",
        "padding": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
    })

