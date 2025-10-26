import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
import datetime


def plot_vix():
    st.subheader("VIX Index Overview")
    # Example plot
    fig, ax = plt.subplots()
    ax.plot([10, 20, 30], [15, 25, 10], label="VIX")
    ax.set_title("VIX Sample Plot")
    ax.legend()
    st.pyplot(fig)

def plot_etps():
    st.subheader("Volatility ETPs")
    # Example plot
    fig, ax = plt.subplots()
    ax.bar(["VXX", "UVXY", "SVXY"], [12, 18, 5], color="skyblue")
    ax.set_title("ETP Performance")
    st.pyplot(fig)

def plot_strategies():
    st.subheader("Volatility Strategies")
    # Example plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [0.5, 0.7, 0.6], marker="o", label="Strategy Alpha")
    ax.set_title("Strategy Signal Strength")
    ax.legend()
    st.pyplot(fig)

def plot_vix_term_structure():
    import streamlit as st
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import requests
    from urllib.parse import unquote
    import datetime

    def fetch_vix_data():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        }
        url = 'https://www.barchart.com/proxies/core-api/v1/quotes/get?'
        with requests.Session() as req:
            req.headers.update(headers)
            r = req.get(url[:25])
            req.headers.update({'X-XSRF-TOKEN': unquote(r.cookies.get_dict()['XSRF-TOKEN'])})
            params = {
                "list": "futures.contractInRoot",
                'root': 'VI',
                "fields": "symbol,symbolName,lastPrice",
                "orderBy": "expiration",
                "orderDir": "desc",
                "between(lastPrice,.10,)": "",
                "between(tradeTime,2024-01-01,2024-12-30)": "",
                "page": "1",
                "limit": "500",
                "raw": "1"
            }
            r = req.get(url, params=params).json()
            return pd.DataFrame(r['data'])

    st.subheader("📈 VIX Futures Term Structure")

    if st.button("🔄 Refresh VIX Data"):
        st.session_state.vix_data = fetch_vix_data()

    # Load data from session or fetch initially
    if "vix_data" not in st.session_state:
        st.session_state.vix_data = fetch_vix_data()

    df = st.session_state.vix_data
    symbols = []
    prices = []

    for _, row in df.iterrows():
        symbols.append(row['symbol'])
        prices.append(float(row['lastPrice'].replace("s", "")))

    x = np.arange(len(prices))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, prices, color='orange', marker='o', markersize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(symbols, fontsize=8)
    for i, j in zip(x, prices):
        ax.annotate(f"{j:.2f}", (i, j), xytext=(0, 5), textcoords='offset points', ha='center', fontsize=8)

    ax.set_xlabel("Symbol")
    ax.set_ylabel("Price")
    ax.set_title("VIX Term Structure")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.text(0.99, 0.01, timestamp, ha='right', transform=ax.transAxes, fontsize=9)

    st.pyplot(fig)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime

def plot_vix_with_sma():
    st.subheader("📉 VIX Chart mit SMA-Linien")

    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=365)
    vix = yf.download("^VIX", start=start, end=end)

    vix["SMA5"] = vix["Close"].rolling(window=5).mean()
    vix["SMA22"] = vix["Close"].rolling(window=22).mean()
    vix["SMA66"] = vix["Close"].rolling(window=66).mean()
    vix["SMA200"] = vix["Close"].rolling(window=200).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(vix.index, vix["Close"], label="VIX", color="orange")
    ax.plot(vix.index, vix["SMA5"], label="SMA 5", linestyle="--", color="blue")
    ax.plot(vix.index, vix["SMA22"], label="SMA 22", linestyle="--", color="green")
    ax.plot(vix.index, vix["SMA66"], label="SMA 66", linestyle="--", color="purple")
    ax.plot(vix.index, vix["SMA200"], label="SMA 200", linestyle="--", color="red")
    ax.set_title("VIX Index ")
    ax.set_ylabel("Indexwert")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
