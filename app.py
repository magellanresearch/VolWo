import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import os

from modules.data_loader import fetch_recent_data, fetch_full_history
from modules.fear_greed_updater import update_fear_greed

TICKERS = ['^VIX', 'UVXY', 'VXX', 'SVXY', 'VXY']
DATA_DIR = "C:/Magellan/VolWo/program/database"
os.makedirs(DATA_DIR, exist_ok=True)

# Auto-update on startup
for ticker in TICKERS:
    try:
        df = fetch_recent_data(ticker)
        df.to_csv(f"{DATA_DIR}/{ticker}_recent.csv")
    except Exception as e:
        print(f"❌ Failed to fetch {ticker}: {e}")

update_fear_greed(
    csv_in=f"{DATA_DIR}/fear-greed.csv",
    csv_out=f"{DATA_DIR}/all_fng_csv.csv",
    pckl_out=f"{DATA_DIR}/all_fng.pkl"
)

# Dash setup
app = dash.Dash(__name__)
app.title = "Volatility Dashboard"

app.layout = html.Div([
    html.H1("Volatility Research Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Button("Download Full History", id="download-btn", n_clicks=0),
        html.Div(id="download-status", style={'marginTop': '10px'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        html.H3("Fear & Greed Index Over Time"),
        dcc.Graph(id="fear-greed-chart")
    ])
])

@app.callback(
    Output("download-status", "children"),
    Input("download-btn", "n_clicks")
)
def manual_download(n_clicks):
    if n_clicks > 0:
        for ticker in TICKERS:
            try:
                df = fetch_full_history(ticker)
                df.to_csv(f"{DATA_DIR}/{ticker}_full.csv")
            except Exception as e:
                print(f"❌ Failed to download full history for {ticker}: {e}")
        return "✅ Historische Daten wurden gespeichert."
    return ""

@app.callback(
    Output("fear-greed-chart", "figure"),
    Input("download-btn", "n_clicks")
)
def update_chart(_):
    df_path = f"{DATA_DIR}/all_fng_csv.csv"
    if not os.path.exists(df_path):
        return {}
    df = pd.read_csv(df_path, parse_dates=["Date"])
    fig = {
        'data': [{
            'x': df['Date'],
            'y': df['Fear Greed'],
            'type': 'line',
            'name': 'Fear & Greed'
        }],
        'layout': {
            'title': 'Fear & Greed Index Over Time',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Index Value'}
        }
    }
    return fig

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
