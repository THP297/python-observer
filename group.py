from dash import html
import pandas as pd
from query_du_lieu import get_group_list
# Dữ liệu mẫu

def render_group_overview(group_data=None):
    if group_data is None:
        group_data = get_group_list()
    return html.Div(
        id="group-overview",
        children=[
            html.Table(
                [
                    html.Thead(html.Tr([html.Th(col) for col in group_data.columns])),
                    html.Tbody(
                        [
                            html.Tr(
                                [
                                    html.Td(group_data.iloc[i][col]) for col in group_data.columns
                                ],
                                style={
                                    "backgroundColor": "#FFA500"  # màu cam
                                } if group_data.iloc[i]["Group"] == "Tổng" else {}
                            )
                            for i in range(len(group_data))
                        ]
                    ),
                ],
                style={
                    "width": "100%",
                    "borderCollapse": "collapse",
                    "textAlign": "center",
                    "marginBottom": "20px",
                    "border": "1px solid #ddd",
                    "padding": "8px",
                },
            )
        ]
    )
