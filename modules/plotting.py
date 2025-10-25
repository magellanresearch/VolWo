import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

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
