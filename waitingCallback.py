
from dash import html, dcc, Output, Input,State
import dash




def applyFilter(filters, filtered_data):
    filter_map = {
        "sdt_filter": lambda data, value: data[data["SĐT"].str.contains(value, case=False, na=False)],
        "agent_filter": lambda data, value: data[data["Agent"].str.contains(value, case=False, na=False)],
        "hang_filter": lambda data, value: data[data["Hạng KH"] == value],
        "huong_filter": lambda data, value: data[data["Hướng"] == value],
        "trangthai_filter": lambda data, value: data[data["Trạng thái"] == value],
        "queue_filter": lambda data, value: data[data["Queue"] == value],
    }

    for key, value in filters.items():
        if key in filter_map and value:
            filtered_data = filter_map[key](filtered_data, value)

    table_rows = []

    for i, row in filtered_data.iterrows():
        # Create a unique key using SĐT and Trạng thái
        unique_key = f"{row['SĐT']}_{row['Trạng thái']}"

        # Generate unique IDs for action buttons and menus
        action_button_id = {"type": "waiting-action-button", "key": unique_key}
        action_menu_id = {"type": "waiting-action-menu", "key": unique_key}

        action_cell = html.Td([
            html.Div(
                [
                    # Action button with a unique ID
                    html.Button(
                        [html.I(className="fas fa-cog")],
                        id=action_button_id,
                        n_clicks=0,
                        style={
                            "backgroundColor": "transparent",
                            "border": "none",
                            "cursor": "pointer",
                            "fontSize": "16px",
                        },
                    ),
                    # Dropdown menu with a unique ID
                    html.Div(
                        id=action_menu_id,
                        style={
                            "width": "300px",
                            "position": "absolute",
                            "zIndex": "10",
                            "backgroundColor": "white",
                            "boxShadow": "0px 4px 8px rgba(0,0,0,0.1)",
                            "padding": "5px",
                            "border": "1px solid #ccc",
                            "left": "100%",
                            "top": "0",
                            "display": "none",
                        },
                        children=[
                            html.Button(
                                "Tham gia",
                                id={"type": "action-thamgia", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Nghe",
                                id={"type": "action-nghe", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Ngắt",
                                id={"type": "action-ngat", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Thì thầm",
                                id={"type": "action-thitham", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Chuyển cuộc gọi",
                                id={"type": "action-chuyencuocgoi", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Chuyển đến bản thân",
                                id={"type": "action-chuyendenbanthan", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                        ],
                    ),
                ],
                style={"position": "relative"},
            )
        ])

        row_html = html.Tr(
            [action_cell] +
            [html.Td(row[col], style={"border": "1px solid #000", "padding": "8px"}) for col in filtered_data.columns],
            key=unique_key,
        )
        table_rows.append(row_html)

    return html.Table([
        html.Thead(html.Tr([
            html.Th("", style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}),
            *[html.Th(col, style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}) for col in filtered_data.columns],
        ])),
        html.Tbody(table_rows),
    ], style={
        "width": "100%",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginBottom": "20px",
        "border": "1px solid #000",
        "padding": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
    })


def render_data(current_data):
    table_rows = []

    for i, row in current_data.iterrows():
        # Create a unique key using SĐT and Trạng thái
        unique_key = f"{row['SĐT']}_{row['Trạng thái']}"

        # Generate unique IDs for action buttons and menus
        action_button_id = {"type": "waiting-action-button", "key": unique_key}
        action_menu_id = {"type": "waiting-action-menu", "key": unique_key}

        action_cell = html.Td([
            html.Div(
                [
                    # Action button with a unique ID
                    html.Button(
                        [html.I(className="fas fa-cog")],
                        id=action_button_id,
                        n_clicks=0,
                        style={
                            "backgroundColor": "transparent",
                            "border": "none",
                            "cursor": "pointer",
                            "fontSize": "16px",
                        },
                    ),
                    # Dropdown menu with a unique ID
                    html.Div(
                        id=action_menu_id,
                        style={
                            "width": "300px",
                            "position": "absolute",
                            "zIndex": "10",
                            "backgroundColor": "white",
                            "boxShadow": "0px 4px 8px rgba(0,0,0,0.1)",
                            "padding": "5px",
                            "border": "1px solid #ccc",
                            "left": "100%",
                            "top": "0",
                            "display": "none",
                        },
                        children=[
                            html.Button(
                                "Tham gia",
                                id={"type": "action-thamgia", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Nghe",
                                id={"type": "action-nghe", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Ngắt",
                                id={"type": "action-ngat", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Thì thầm",
                                id={"type": "action-thitham", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Chuyển cuộc gọi",
                                id={"type": "action-chuyencuocgoi", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                            html.Button(
                                "Chuyển đến bản thân",
                                id={"type": "action-chuyendenbanthan", "key": unique_key},
                                n_clicks=0,
                                style={"width": "100%", "padding": "5px", "border": "none", "cursor": "pointer"}
                            ),
                        ],
                    ),
                ],
                style={"position": "relative"},
            )
        ])

        row_html = html.Tr(
            [action_cell] +
            [html.Td(row[col], style={"border": "1px solid #000", "padding": "8px"}) for col in current_data.columns],
            key=unique_key,
        )
        table_rows.append(row_html)

    return html.Table([
        html.Thead(html.Tr([
            html.Th("", style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}),
            *[html.Th(col, style={"border": "1px solid #000", "padding": "8px", "fontWeight": "bold"}) for col in
              current_data.columns],
        ])),
        html.Tbody(table_rows),
    ], style={
        "width": "100%",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginBottom": "20px",
        "border": "1px solid #000",
        "padding": "8px",
        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
    })

