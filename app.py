import streamlit as st
import pandas as pd
import os

from modules.data_loader import fetch_recent_data, fetch_full_history
from modules.fear_greed_updater import update_fear_greed

TICKERS = ['^VIX', 'UVXY', 'VXX', 'SVXY', 'VXY']
DATA_DIR = "database"
os.makedirs(DATA_DIR, exist_ok=True)

# Auto-update on startup
st.sidebar.success("🔄 Updating recent data...")
for ticker in TICKERS:
    try:
        df = fetch_recent_data(ticker)
        df.to_csv(f"{DATA_DIR}/{ticker}_recent.csv")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to fetch {ticker}: {e}")

update_fear_greed(
    csv_in=f"{DATA_DIR}/fear-greed.csv",
    csv_out=f"{DATA_DIR}/all_fng_csv.csv",
    pckl_out=f"{DATA_DIR}/all_fng.pkl"
)

# Layout
st.title("📈 Volatility Research Dashboard")

# Download button
if st.button("📥 Download Full History"):
    for ticker in TICKERS:
        try:
            df = fetch_full_history(ticker)
            df.to_csv(f"{DATA_DIR}/{ticker}_full.csv")
        except Exception as e:
            st.error(f"❌ Failed to download full history for {ticker}: {e}")
    st.success("✅ Historische Daten wurden gespeichert.")

# Fear & Greed Chart
st.subheader("📊 Fear & Greed Index Over Time")
try:
    df_fng = pd.read_pickle(f"{DATA_DIR}/all_fng.pkl")
    st.line_chart(df_fng.set_index("date")["value"])
except Exception as e:
    st.warning(f"⚠️ Could not load chart: {e}")
