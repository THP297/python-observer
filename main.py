from dash import dcc, html, Output, Input, State
from group import render_group_overview
from waiting import render_waiting_calls, register_callbacks as waiting_callbacks
from agent import render_agent_list
from report import render_agent_summary
from ongoing import render_ongoing_calls, register_callbacks as ongoing_callbacks
from query_du_lieu import get_user_list,get_group_list,get_ongoing_3cx,get_waiting_3cx
from flask_caching import Cache  # Thêm thư viện cache
import dash


# Khởi tạo ứng dụng Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ],suppress_callback_exceptions=True
)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Bạn có thể dùng 'redis' hoặc 'filesystem' nếu cần lưu trữ phức tạp hơn
    'CACHE_DEFAULT_TIMEOUT': 1  # Cache timeout (giây)
})

@cache.memoize()
def load_data_agent():
    return get_user_list()
@cache.memoize()
def load_data_group():
    return get_group_list()
@cache.memoize()
def load_waiting_call():
    return get_waiting_3cx()

# Layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    # Hai nút điều khiển
    html.Div(
        className="row d-flex justify-content-between",
        style={"position": "relative", "width": "100%", "height": "50px", "padding": "10px 0"},
        children=[
            html.Div(
                id="leftButton",
                className="custom-btn",
                style={"position": "absolute", "left": "10px", "top": "10px", "cursor": "pointer"},
                children=html.I(className="fas fa-arrow-up", style={"fontSize": "20px"})
            ),
            html.Div(
                id="rightButton",
                className="custom-btn",
                style={"position": "absolute", "right": "10px", "top": "10px", "cursor": "pointer"},
                children=html.I(className="fas fa-arrow-right", style={"fontSize": "20px"})
            )
        ]
    ),

    # Phần nội dung chính
    html.Div(
        className="row",
        style={"display": "flex", "flexWrap": "nowrap", "width": "100%"},
        children=[
            # Cột bên trái
            html.Div(
                id="left-panel",
                style={"width": "64%", "borderRight": "1px solid #ccc", "padding": "10px"},
                children=[
                    # Bảng Tổng quan nhóm
                    render_group_overview(),

                    # Cuộc gọi đang diễn ra
                    render_ongoing_calls(),

                    # Cuộc gọi đang chờ
                    render_waiting_calls()
                ]
            ),

            # Cột bên phải
            html.Div(
                id="right-panel",
                style={"width": "34%", "padding": "10px"},
                children=[
                    # Bảng danh sách agent
                    render_agent_list(agent_data=None),

                    # Bảng tóm tắt agent
                    render_agent_summary()
                ]
            )
        ]
    ),
    dcc.Interval(
        id="interval-component",
        interval=1000,  # Khoảng thời gian (ms), 1000ms = 1s
        n_intervals=0  # Đếm số lần kích hoạt, mặc định là 0
    )
])


# Callback cho hai nút hành động
@app.callback(
    [
        Output("group-overview", "style"),
        Output("leftButton", "children"),
        Output("right-panel", "style"),
        Output("rightButton", "children"),
        Output("left-panel", "style"),  # Thêm style cho left-panel
    ],
    [
        Input("leftButton", "n_clicks"),
        Input("rightButton", "n_clicks")
    ],
    [
        State("group-overview", "style"),
        State("right-panel", "style"),
        State("left-panel", "style")
    ]
)
def toggle_panels(left_clicks, right_clicks, group_style, right_style, left_style):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Xử lý nút leftButton
    if button_id == "leftButton":
        if group_style and group_style.get("display") == "none":
            return (
                {},  # Hiện group-overview
                html.I(className="fas fa-arrow-up", style={"fontSize": "20px"}),
                right_style,
                html.I(className="fas fa-arrow-right", style={"fontSize": "20px"}),
                left_style  # Giữ nguyên left-panel
            )
        else:
            return (
                {"display": "none"},  # Ẩn group-overview
                html.I(className="fas fa-arrow-down", style={"fontSize": "20px"}),
                right_style,
                html.I(className="fas fa-arrow-right", style={"fontSize": "20px"}),
                left_style  # Giữ nguyên left-panel
            )

    # Xử lý nút rightButton
    if button_id == "rightButton":
        if right_style and right_style.get("display") == "none":
            return (
                group_style,
                html.I(className="fas fa-arrow-up", style={"fontSize": "20px"}),
                {"width": "34%", "padding": "10px"},  # Hiện lại right-panel
                html.I(className="fas fa-arrow-right", style={"fontSize": "20px"}),
                {"width": "64%", "borderRight": "1px solid #ccc", "padding": "10px"}  # Left-panel trở lại 64%
            )
        else:
            return (
                group_style,
                html.I(className="fas fa-arrow-up", style={"fontSize": "20px"}),
                {"display": "none"},  # Ẩn right-panel
                html.I(className="fas fa-arrow-left", style={"fontSize": "20px"}),
                {"width": "100%", "padding": "10px"}  # Left-panel chiếm toàn bộ màn hình
            )

    return group_style, html.I(className="fas fa-arrow-up", style={"fontSize": "20px"}), right_style, html.I(className="fas fa-arrow-right", style={"fontSize": "20px"}), left_style

@app.callback(
    Output("agent-list", "children"),  # Đầu ra là nội dung của agent-list
    Input("interval-component", "n_intervals")  # Kích hoạt mỗi khi interval chạy
)
def update_agent(n_intervals):
    # Tải dữ liệu mới và trả về nội dung của agent-list
    # Bạn có thể thay thế logic này bằng truy vấn cơ sở dữ liệu hoặc API
    agent_data = load_data_agent()
    #print(f"update_agent_list {n_intervals}")
    return render_agent_list(agent_data).children

@app.callback(
    Output("group-overview", "children"),  # Đầu ra là nội dung của agent-list
    Input("interval-component", "n_intervals")  # Kích hoạt mỗi khi interval chạy
)
def update_group(n_intervals):
    # Tải dữ liệu mới và trả về nội dung của agent-list
    # Bạn có thể thay thế logic này bằng truy vấn cơ sở dữ liệu hoặc API
    group_data = load_data_group()
    #print(f"update_agent_list {n_intervals}")
    return render_group_overview(group_data).children

# Đăng ký callbacks cho các phần khác
# ongoing_callbacks(app)
waiting_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
