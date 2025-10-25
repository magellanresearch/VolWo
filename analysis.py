import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_data():
    st.subheader("🔍 Data Analyzer")

    # Simulated input (replace with real data loading)
    dates = pd.date_range(start="2023-01-01", periods=100)
    values = np.random.normal(loc=0, scale=1, size=100)
    df = pd.DataFrame({"Date": dates, "Signal": values})

    # Signal detection logic
    threshold = st.slider("Signal Threshold", min_value=0.0, max_value=3.0, value=1.5)
    df["Detected"] = df["Signal"].apply(lambda x: "High" if abs(x) > threshold else "Normal")

    # Display table
    st.dataframe(df)

    # Plot signals
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Signal"], label="Signal")
    ax.axhline(threshold, color="red", linestyle="--", label="Threshold")
    ax.axhline(-threshold, color="red", linestyle="--")
    ax.set_title("Signal Detection")
    ax.legend()
    st.pyplot(fig)
