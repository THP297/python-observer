import pandas as pd
from dash import html, Output, Input
from dash import Dash

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.Button("Button 1", id="button-1", n_clicks=0),
    html.Button("Button 2", id="button-2", n_clicks=0),
    html.Div(id="output-text", children="Output will appear here.")
])

@app.callback(
    Output("output-text", "children"),
    Input("button-1", "n_clicks")
)
def update_from_button_1(n_clicks):
    if n_clicks > 0:
        return f"Button 1 clicked {n_clicks} times"

@app.callback(
    Output("output-text", "children"),
    Input("button-2", "n_clicks")
)
def update_from_button_2(n_clicks):
    if n_clicks > 0:
        return f"Button 2 clicked {n_clicks} times"

if __name__ == "__main__":
    app.run_server(debug=True)
