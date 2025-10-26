import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_vix_term_structure(vix_futures_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    for date in vix_futures_df['Date'].unique():
        subset = vix_futures_df[vix_futures_df['Date'] == date]
        ax.plot(subset['Maturity'], subset['Price'], label=str(date))
    ax.set_title("VIX Futures Term Structure")
    ax.set_xlabel("Maturity")
    ax.set_ylabel("Price")
    ax.legend(fontsize="small", loc="upper left")
    ax.grid(True)
    return fig

def plot_vix_with_sma(vix_df: pd.DataFrame, sma_periods=(20, 50)):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(vix_df['Date'], vix_df['VIX'], label="VIX", color="black")
    for period in sma_periods:
        sma = vix_df['VIX'].rolling(window=period).mean()
        ax.plot(vix_df['Date'], sma, label=f"SMA {period}")
    ax.set_title("VIX mit SMA-Overlays")
    ax.set_xlabel("Datum")
    ax.set_ylabel("VIX")
    ax.legend()
    ax.grid(True)
    return fig
