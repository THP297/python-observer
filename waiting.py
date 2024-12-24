from dash import html, dcc, Output, Input,State
from dash.dependencies import Input, Output, State, MATCH,ALL
import pandas as pd
import hashlib
import dash
from waitingCallback import  applyFilter, render_data

cached_rows = {}
# Global variable to store the previous data hash
previous_data_hash = None

# Dữ liệu mẫu cho "Cuộc gọi đang chờ"
waiting_calls_data = pd.DataFrame({
    "Hướng": ["Inbound", "Outbound", "Callback", "Campaign"],
    "Thời gian": ["00:01:23", "00:03:45", "00:02:10", "00:04:30"],
    "SĐT": ["0987654321", "0912345678", "0901111222", "0911223344"],
    "KH": ["Client A", "Client B", "Client C", "Client D"],
    "Hạng KH": ["Titan", "Gold", "Silver", "Titan"],
    "Agent": ["Agent 1", "Agent 2", "Agent 3", "Agent 5"],
    "Queue": ["Sales", "Support", "Tech", "Marketing"],
    "Trạng thái": ["Transfering", "Routing", "Transfering", "Routing"]
})


def get_updated_row_data(filters):
    # Apply filters to find the matching row in the data
    filtered_data = waiting_calls_data

    if filters["sdt_filter"]:
        filtered_data = filtered_data[filtered_data["SĐT"].str.contains(filters["sdt_filter"], case=False, na=False)]
    if filters["agent_filter"]:
        filtered_data = filtered_data[filtered_data["Agent"].str.contains(filters["agent_filter"], case=False, na=False)]
    if filters["hang_filter"]:
        filtered_data = filtered_data[filtered_data["Hạng KH"] == filters["hang_filter"]]
    if filters["huong_filter"]:
        filtered_data = filtered_data[filtered_data["Hướng"] == filters["huong_filter"]]
    if filters["trangthai_filter"]:
        filtered_data = filtered_data[filtered_data["Trạng thái"] == filters["trangthai_filter"]]
    if filters["queue_filter"]:
        filtered_data = filtered_data[filtered_data["Queue"] == filters["queue_filter"]]

    # Return the first matching row as a dictionary
    if not filtered_data.empty:
        return filtered_data.iloc[0].to_dict()
    else:
        return {"SĐT": "N/A", "Trạng thái": "N/A", "Agent": "N/A", "Queue": "N/A"}

def render_waiting_calls():
    return html.Div([
        html.Div([
            html.Button(
                id="toggleFiltersBtn2",
                className="filter-btn btn mb-3",
                children=[
                    html.I(className="fas fa-filter", style={"color": "#864f10", "marginRight": "10px"}),
                    html.H2(
                        "Cuộc gọi đang chờ",
                        className="text-left text-center px-3 m-0",
                        style={"display": "inline-block", "margin": "0", "color": "white"}
                    )
                ],
                style={
                    "display": "block",
                    "margin": "0 auto",
                    "width": "100%",
                    "padding": "5px 20px",
                    "borderRadius": "5px",
                    "backgroundColor": "#f9a01b",
                    "border": "none",
                    "cursor": "pointer"
                }
            ),
            html.Div(
                id="waiting-filters",
                style={
                    "display": "none",
                    "alignItems": "center",
                    "marginTop": "10px",
                    "gap": "10px",
                    "width": "100%"
                },
                children=[
                    dcc.Dropdown(
                        id="filter-waiting-huong",
                        options=[
                            {"label": "Inbound", "value": "Inbound"},
                            {"label": "Outbound", "value": "Outbound"},
                            {"label": "Callback", "value": "Callback"},
                            {"label": "Campaign", "value": "Campaign"}
                        ],
                        placeholder="Lọc theo hướng",
                        style={"flex": "1", "height": "40px"}
                    ),
                    dcc.Dropdown(
                        id="filter-waiting-hang",
                        options=[
                            {"label": "Titan", "value": "Titan"},
                            {"label": "Gold", "value": "Gold"},
                            {"label": "Silver", "value": "Silver"}
                        ],
                        placeholder="Lọc theo hạng KH",
                        style={"flex": "1", "height": "40px"}
                    ),
                    dcc.Dropdown(
                        id="filter-waiting-trangthai",
                        options=[
                            {"label": "Transfering", "value": "Transfering"},
                            {"label": "Routing", "value": "Routing"}
                        ],
                        placeholder="Lọc theo trạng thái",
                        style={"flex": "1", "height": "40px"}
                    ),
                    dcc.Input(
                        id="filter-waiting-sdt",
                        type="text",
                        placeholder="Lọc theo SĐT",
                        style={"flex": "1", "height": "40px", "padding": "5px"}
                    ),
                    dcc.Input(
                        id="filter-waiting-agent",
                        type="text",
                        placeholder="Lọc theo Agent",
                        style={"flex": "1", "height": "40px", "padding": "5px"}
                    ),
                    dcc.Input(
                        id="filter-waiting-queue",
                        type="text",
                        placeholder="Lọc theo Queue",
                        style={"flex": "1", "height": "40px", "padding": "5px"}
                    )
                ]
            )
        ], style={"marginBottom": "20px"}),

        html.Div(
            id="waiting-table",
            style={"marginTop": "20px", "height": "200px", "overflow": "auto"},
            children=[]
        )
    ])

def register_callbacks(app):

    @app.callback(
        Output("waiting-table", "children"),
        [
            Input("filter-waiting-huong", "value"),
            Input("filter-waiting-hang", "value"),
            Input("filter-waiting-trangthai", "value"),
            Input("filter-waiting-sdt", "value"),
            Input("filter-waiting-agent", "value"),
            Input("filter-waiting-queue", "value"),
            Input("interval-component", "n_intervals")
        ],
        [State("waiting-table", "children")],
    )


    def update_waiting_table(huong_filter, hang_filter, trangthai_filter, sdt_filter, agent_filter, queue_filter, n_intervals, table_children):
        global cached_rows
        # Only proceed if table children is empty
        if table_children:
            return table_children

        filtered_data = waiting_calls_data

        # Prepare filters as a dictionary
        filters = {
            "huong_filter": huong_filter,
            "hang_filter": hang_filter,
            "trangthai_filter": trangthai_filter,
            "sdt_filter": sdt_filter,
            "agent_filter": agent_filter,
            "queue_filter": queue_filter,
        }

        print(filters)
        # Check if there is at least one filter value
        if any(filters.values()):
            print("wtf")
            # Apply filters using hash table
            filtered_data = applyFilter(filters, filtered_data)
            return filtered_data


        # Load the current waiting calls data
        current_data = waiting_calls_data

        # Compute hash of the current data
        current_data_hash = hashlib.md5(str(current_data).encode('utf-8')).hexdigest()

        # Check if the data has changed
        if current_data_hash != previous_data_hash:

            return render_data(current_data)

    @app.callback(
        Output({"type": "waiting-row", "key": MATCH}, "children"),
        [
            Input("filter-waiting-huong", "value"),
            Input("filter-waiting-hang", "value"),
            Input("filter-waiting-trangthai", "value"),
            Input("filter-waiting-sdt", "value"),
            Input("filter-waiting-agent", "value"),
            Input("filter-waiting-queue", "value"),
            Input("interval-component", "n_intervals")
        ],
        [State({"type": "waiting-row", "key": MATCH}, "children"),
         State({"type": "waiting-row", "key": MATCH}, "id")]
    )
    def update_specific_row(huong_filter, hang_filter, trangthai_filter, sdt_filter, agent_filter, queue_filter,
                            n_intervals, row_children, row_id):
        # Extract the key of the specific row
        print(row_id)
        row_key = row_id["key"]

        # Prepare filters as a dictionary
        filters = {
            "huong_filter": huong_filter,
            "hang_filter": hang_filter,
            "trangthai_filter": trangthai_filter,
            "sdt_filter": sdt_filter,
            "agent_filter": agent_filter,
            "queue_filter": queue_filter,
        }

        # Apply filters to find the updated row for this specific key
        updated_row_data = get_updated_row_data(filters)

        # Check if the specific key matches the updated data (to avoid unnecessary updates)
        if updated_row_data["SĐT"] != row_key.split("_")[0]:  # Assuming key is based on `SĐT`
            return row_children

        # Construct updated row
        updated_row = html.Tr([
            html.Td(updated_row_data["SĐT"], style={"border": "1px solid #000", "padding": "8px"}),
            html.Td(updated_row_data["Trạng thái"], style={"border": "1px solid #000", "padding": "8px"}),
            html.Td(updated_row_data["Agent"], style={"border": "1px solid #000", "padding": "8px"}),
            html.Td(updated_row_data["Queue"], style={"border": "1px solid #000", "padding": "8px"}),
        ])

        return updated_row

    @app.callback(
        Output({"type": "waiting-action-menu", "key": ALL}, "style"),  # Update all menus
        [Input({"type": "waiting-action-button", "key": ALL}, "n_clicks")],  # Monitor all buttons
        [State({"type": "waiting-action-menu", "key": ALL}, "style")],  # Track menu styles
        prevent_initial_call=True,
    )
    def toggle_specific_menu(n_clicks, current_styles):
        ctx = dash.callback_context

        if not ctx.triggered:
            # Default: Hide all menus
            return [{"display": "none"} for _ in current_styles]

        # Identify the triggered button
        triggered_prop_id = ctx.triggered[0][
            "prop_id"]  # e.g., '{"type":"action-button","key":"0987654321_Transfering"}.n_clicks'
        triggered_id = eval(triggered_prop_id.split(".")[0])  # Extract the dictionary
        triggered_key = triggered_id["key"]  # Extract the 'key'

        # Generate new styles for all menus
        new_styles = []
        for i, style in enumerate(current_styles):
            # Match the menu's key to the triggered key
            menu_key = ctx.outputs_list[i]["id"]["key"]
            if menu_key == triggered_key:
                # Toggle visibility for the triggered menu with additional styles
                if style.get("display") == "none":
                    new_styles.append({
                        "display": "block",
                        "width": "300px",
                        "position": "absolute",
                        "zIndex": "10",
                        "backgroundColor": "white",
                        "boxShadow": "0px 4px 8px rgba(0,0,0,0.1)",
                        "padding": "5px",
                        "border": "1px solid #ccc",
                        "left": "100%",
                        "top": "0",
                    })
                else:
                    new_styles.append({"display": "none"})
            else:
                # Hide all other menus
                new_styles.append({"display": "none"})

        return new_styles

    @app.callback(
    Output("waiting-filters", "style"),
    [Input("toggleFiltersBtn2", "n_clicks")],
    [State("waiting-filters", "style")]
    )

    def toggle_filters(n_clicks, current_style):
        # Style mặc định
        default_style = {
            "display": "none",  # Ẩn mặc định
            "alignItems": "center",
            "marginTop": "10px",
            "gap": "10px",
            "width": "100%"
        }

        # Nếu chưa nhấn nút hoặc style chưa khởi tạo, trả về mặc định
        if n_clicks is None or current_style is None:
            return default_style

        # Cập nhật trạng thái `display`
        if current_style.get("display") == "none":
            current_style["display"] = "flex"
        else:
            current_style["display"] = "none"

        return current_style





