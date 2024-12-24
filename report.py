from dash import html
import pandas as pd

# Dữ liệu mẫu cho "Danh sách agent"
agent_data = pd.DataFrame({
    "STT": [1, 2, 3, 4, 5, 6, 7, 8],
    "Số nội bộ": [10022, 10015, 10012, 10003, 10004, 11179, 10021, 10013],
    "Tổng đài viên": ["admin", "alex", "testest", "supervisor", "leonard", "roger_test", "user3", "user2"],
    "Trạng thái": ["Available", "Available", "Available", "Campaign", "Outbound", "Outbound", "Meeting", "Meeting"],
    "Thời gian": ["07:20:46", "07:15:04", "07:12:13", "01:54:33", "06:43:37", "00:00:00", "00:00:00", "14:14:34"],
    "Nhóm": ["Admin", "Admin", "Admin", "Supervisor", "BO", "Manager", "Agent_LPB", "Manager"]
})

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

def render_agent_list():
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
    ], style={
        "width": "100%",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginBottom": "20px",
        "border": "1px solid #000",
        "padding": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
    })

# Dữ liệu mẫu cho "Agent Summary"
agent_summary_data = pd.DataFrame({
    "STT": [1, 2, 3, 4, 5],
    "Agent": ["admin", "alex", "testest", "supervisor", "leonard"],
    "NS Lũy kế": [10, 20, 15, 8, 12],
    "Not Answer": [0, 1, 0, 2, 3],
    "Chưa login": [0, 0, 0, 0, 1],
    "Tổng thời gian vi phạm": ["00:00:00", "00:01:23", "00:00:00", "00:03:45", "00:00:00"],
    "No ACD": [0, 0, 1, 0, 0],
    "Meeting": [0, 1, 0, 0, 0],
    "Lunch": [0, 0, 0, 0, 0],
    "Login": [8, 7, 7, 6, 5],
    "Outbound": [1, 2, 0, 1, 2]
})

def render_agent_summary():
    table_rows = [
        html.Tr([
            *[
                html.Td(
                    agent_summary_data.iloc[i][col],
                    style={
                        "border": "1px solid #000",
                        "padding": "8px"
                    }
                ) for col in agent_summary_data.columns
            ]
        ], style={"border": "1px solid #000"})
        for i in range(len(agent_summary_data))
    ]

    return html.Table([
        html.Thead(html.Tr([
            *[html.Th(col, style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}) for col in agent_summary_data.columns]
        ], style={"border": "1px solid #000"})),
        html.Tbody(table_rows)
    ], style={
        "width": "100%",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginBottom": "20px",
        "border": "1px solid #000",
        "padding": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"
    })
