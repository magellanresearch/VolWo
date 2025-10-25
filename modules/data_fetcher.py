import yfinance as yf
import pandas as pd

def fetch_data(tickers=["^vix", "VXX", "UVXY", "SVXY"], period="max"):
    all_data = {}
    for ticker in tickers:
        df = yf.download(ticker, period=period)
        df = df.dropna()
        df["Return"] = df["Close"].pct_change()
        all_data[ticker] = df
    return all_data
