import yfinance as yf
import pandas as pd
from scipy import stats
from datetime import datetime

def fetch_recent_data(ticker, days=5):
    end = datetime.today()
    start = end - pd.Timedelta(days=days)
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
    return clean_data(df)

def fetch_full_history(ticker):
    df = yf.download(ticker, start='2005-01-01', end=datetime.today().strftime('%Y-%m-%d'))
    return clean_data(df)

def clean_data(df):
    df = df.interpolate(method='linear').bfill().ffill()
    df['Outlier'] = False

    if 'Close' in df.columns and not df['Close'].dropna().empty:
        close_series = df['Close'].dropna()
        z_scores = stats.zscore(close_series)
        outlier_mask = abs(z_scores) > 3
        outlier_dates = close_series[outlier_mask].index
        df.loc[df.index.isin(outlier_dates), 'Outlier'] = True
        print(f"Outliers detected on: {list(outlier_dates)}")

    return df
