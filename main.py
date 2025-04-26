import dash
from dash import dcc, html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import datetime
import random

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Example data storage for the graph
graph_data = {
    "x": [],  # Timestamps
    "y": []   # Profit values
}

# App layout
app.layout = dbc.Container([
    # Frame 1: PnL and Graph
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("PnL and Graph", style={"background-color": "#2a2a2a", "color": "lime"}),
                dbc.CardBody([
                    dbc.Row([
                        # Labels (30% width) - On the left side
                        dbc.Col([
                            dcc.Loading(
                                id="loading-labels",
                                type="circle",
                                children=html.Div([
                                    html.H5("PnL (%)", id="pnl-percentage-label", style={"color": "lime", "font-size": "20px", "text-align": "center"}),
                                    html.H5("PnL (Absolute)", id="pnl-absolute-label", style={"color": "lime", "font-size": "20px", "text-align": "center", "margin-top": "20px"}),
                                ], style={"height": "100%", "display": "flex", "flex-direction": "column", "justify-content": "center"})
                            )
                        ], width=3),  # 30% width for labels

                        # Graph (70% width) - On the right side
                        dbc.Col([
                            dcc.Loading(
                                id="loading-graph",
                                type="circle",
                                children=dcc.Graph(
                                    id="pnl-graph",
                                    config={"displayModeBar": False},  # Disable unnecessary interactions
                                    style={"height": "400px"},
                                )
                            )
                        ], width=9),  # 70% width for graph
                    ])
                ])
            ], className="mb-4", style={"background-color": "#2a2a2a"})
        ], width=12)
    ]),

    # Frame 2: Watchlist Table
    dcc.Loading(
        id="loading-watchlist",
        type="circle",
        children=dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Stock Watchlist", style={"background-color": "#2a2a2a", "color": "lime"}),
                    dbc.CardBody([
                        html.Div([
                            html.Table(
                                id="watchlist-table",
                                children=[
                                    html.Tr([html.Th("Name"), html.Th("Qty"), html.Th("BPrice"), html.Th("CPrice"), html.Th("PnL"), html.Th("Optional")], style={"color": "lime"}),
                                    # Example rows (replace with dynamic rows)
                                    html.Tr([html.Td("Stock A"), html.Td("10"), html.Td("100"), html.Td("110"), html.Td("10%"), html.Td("-")]),
                                    html.Tr([html.Td("Stock B"), html.Td("5"), html.Td("200"), html.Td("190"), html.Td("-5%"), html.Td("-")]),
                                ],
                                className="table table-dark table-striped",
                                style={"width": "100%"}
                            )
                        ], id="watchlist-container", style={"overflow-y": "auto", "max-height": "400px"})  # Expandable container
                    ])
                ], className="mb-4", style={"background-color": "#2a2a2a"})
            ], width=12)
        ])
    ),

    # Frame 3: Log Text Box
    dcc.Loading(
        id="loading-log",
        type="circle",
        children=dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Log", style={"background-color": "#2a2a2a", "color": "lime"}),
                    dbc.CardBody([
                        dcc.Textarea(
                            id="log-box",
                            value="Log initialized...\n",
                            style={"width": "100%", "height": "200px", "background-color": "#1e1e1e", "color": "white", "border": "1px solid lime"}
                        )
                    ])
                ], className="mb-4", style={"background-color": "#2a2a2a"})
            ], width=12)
        ])
    ),

    # Frame 4: Settings
    dcc.Loading(
        id="loading-settings",
        type="circle",
        children=dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Settings", style={"background-color": "#2a2a2a", "color": "lime"}),
                    dbc.CardBody([
                        # Strategy Switches
                        html.Div([
                            html.Div("Strategies:", style={"color": "lime", "margin-bottom": "10px"}),
                            dbc.Row([
                                dbc.Col(dbc.Switch(id="strategy-1-switch", label="Strategy 1", value=False, style={"color": "lime"}), width=2),
                                dbc.Col(dbc.Switch(id="strategy-2-switch", label="Strategy 2", value=False, style={"color": "lime"}), width=2),
                                dbc.Col(dbc.Switch(id="strategy-3-switch", label="Strategy 3", value=False, style={"color": "lime"}), width=2),
                                dbc.Col(dbc.Switch(id="strategy-4-switch", label="Strategy 4", value=False, style={"color": "lime"}), width=2),
                                dbc.Col(dbc.Switch(id="strategy-5-switch", label="Strategy 5", value=False, style={"color": "lime"}), width=2),
                            ], className="mb-3"),
                        ]),

                        # API Key Input
                        html.Div([
                            html.Div("API Keys:", style={"color": "lime", "margin-bottom": "10px"}),
                            dbc.Row([
                                dbc.Col(dcc.Input(id="dhan-api-key", type="password", placeholder="dhan api key", className="form-control"), width=10),
                                dbc.Col(html.Button("Save Key", id="save-api-key-1", n_clicks=0, className="btn btn-success"), width=2),
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col(dcc.Input(id="upstox-api-key", type="password", placeholder="upstox api key", className="form-control"), width=10),
                                dbc.Col(html.Button("Save Key", id="save-api-key-2", n_clicks=0, className="btn btn-success"), width=2),
                            ], className="mb-3"),
                        ]),

                        # Stop Limit and Fund Limit Inputs
                        html.Div([
                            html.Div("Trade Settings:", style={"color": "lime", "margin-bottom": "10px"}),
                            dbc.Row([
                                dbc.Col(dcc.Input(id="stop-limit", type="number", placeholder="Stop Limit (e.g., -500)", className="form-control"), width=10),
                                dbc.Col(html.Button("Set Limit", id="set-stop-limit", n_clicks=0, className="btn btn-primary"), width=2),
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Col(dcc.Input(id="available-funds", type="number", placeholder="Available Funds (e.g., 10000)", className="form-control"), width=10),
                                dbc.Col(html.Button("Set Funds", id="set-available-funds", n_clicks=0, className="btn btn-primary"), width=2),
                            ], className="mb-3"),
                        ]),

                        # Stock Symbol Input Section
                        html.Div([
                            html.Div("Add Stock Symbols:", style={"color": "lime", "margin-bottom": "10px"}),
                            dbc.Row([
                                dbc.Col(dcc.Input(id="stock-symbols", type="text", placeholder="Enter stock symbols (e.g., AAPL, TSLA)", className="form-control"), width=10),
                                dbc.Col(html.Button("Save Symbols", id="save-stock-symbols", n_clicks=0, className="btn btn-primary"), width=2),
                            ], className="mb-3"),
                        ]),

                        # Start and Stop Buttons
                        html.Div([
                            dbc.Row([
                                dbc.Col(html.Button("Start Algo", id="start-algo", n_clicks=0, className="btn btn-success"), width=6),
                                dbc.Col(html.Button("Stop Algo", id="stop-algo", n_clicks=0, className="btn btn-danger"), width=6, style={"text-align": "right"}),
                            ], className="mt-3"),
                        ]),
                    ])
                ], className="mb-4", style={"background-color": "#2a2a2a"})
            ], width=12)
        ])
    ),

    # Add this to your layout
    dcc.Interval(
        id="interval-component",
        interval=60000,  # Update every 1 minute
        n_intervals=0
    ),

], fluid=True, style={"overflow-y": "scroll", "height": "100vh"})  # Make layout scrollable


@app.callback(
    [Output("pnl-percentage-label", "children"),
     Output("pnl-percentage-label", "style"),
     Output("pnl-absolute-label", "children"),
     Output("pnl-absolute-label", "style")],
    Input("interval-component", "n_intervals")  # Triggered every interval
)
def update_pnl_labels(n_intervals):
    # Example PnL values (replace with actual logic)
    pnl_percentage = random.uniform(-5, 5)  # Example percentage
    pnl_absolute = random.uniform(-1000, 1000)  # Example absolute value

    # Determine colors based on PnL values
    percentage_color = "green" if pnl_percentage >= 0 else "red"
    absolute_color = "green" if pnl_absolute >= 0 else "red"

    # Update labels
    percentage_label = f"PnL: {pnl_percentage:.2f}%"
    absolute_label = f"PnL: ${pnl_absolute:,.2f}"

    return (
        percentage_label, {"color": percentage_color, "font-size": "20px", "text-align": "center"},
        absolute_label, {"color": absolute_color, "font-size": "20px", "text-align": "center"}
    )


@app.callback(
    Output("pnl-graph", "figure"),
    Input("interval-component", "n_intervals")  # Triggered every 1 minute
)
def update_graph(n_intervals):
    # Placeholder for real data (replace this with actual data from TSV or API)
    if len(graph_data["x"]) == 0:  # If no data exists, initialize with placeholders
        graph_data["x"] = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00"]
        graph_data["y"] = [0, 1, -2, 3, -1, 2, 0, 1, -1, 2, 3, -2, 1]

    # Create the figure
    figure = go.Figure(
        data=[
            go.Scatter(
                x=graph_data["x"],
                y=graph_data["y"],
                mode="lines+markers",
                line=dict(color="lime"),
                marker=dict(size=6)
            )
        ],
        layout=go.Layout(
            title="PnL Over Time",
            xaxis=dict(
                title="Time",
                showgrid=True,
                showline=True,
                zeroline=False,
                tickformat="%H:%M",
                rangeslider=dict(visible=True),  # Enable horizontal scrolling
            ),
            yaxis=dict(
                title="Profit",
                zeroline=True,
                zerolinecolor="white",
                zerolinewidth=2,
                showgrid=True,
                showline=True,
                range=[-10, 10],  # Adjust range as needed
            ),
            paper_bgcolor="#1e1e1e",
            plot_bgcolor="#1e1e1e",
            font=dict(color="lime"),
            dragmode=False  # Disable selection zoom
        )
    )

    return figure


@app.callback(
    Output("watchlist-table", "children"),
    Input("save-stock-symbols", "n_clicks"),
    State("stock-symbols", "value"),
    prevent_initial_call=True
)
def update_watchlist(n_clicks, symbols):
    if not symbols:
        raise dash.exceptions.PreventUpdate

    # Split symbols by comma and create rows dynamically
    symbol_list = [symbol.strip() for symbol in symbols.split(",")]
    rows = [
        html.Tr([html.Td(symbol), html.Td("10"), html.Td("100"), html.Td("110"), html.Td("10%"), html.Td("-")])
        for symbol in symbol_list
    ]

    # Add header row
    header = html.Tr([html.Th("Name"), html.Th("Qty"), html.Th("BPrice"), html.Th("CPrice"), html.Th("PnL"), html.Th("Optional")], style={"color": "lime"})

    return [header] + rows


# Run the app
if __name__ == "__main__":
    app.run(debug=True)