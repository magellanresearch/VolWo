import streamlit as st
import pandas as pd
from plotting import plot_vix_term_structure, plot_vix_with_sma

# Dummy-Daten (ersetzen durch echte Datenquellen)
def load_vix_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=100)
    vix = pd.Series(15 + 5 * np.sin(np.linspace(0, 10, 100)), index=dates)
    return pd.DataFrame({'Date': dates, 'VIX': vix})

def load_vix_futures_data():
    base_date = pd.Timestamp.today()
    maturities = [1, 2, 3, 4, 5]
    data = []
    for i in range(3):
        date = base_date - pd.Timedelta(days=i)
        prices = 15 + np.random.rand(len(maturities)) * 5
        for m, p in zip(maturities, prices):
            data.append({'Date': date.date(), 'Maturity': m, 'Price': p})
    return pd.DataFrame(data)

# Daten laden
vix_df = load_vix_data()
vix_futures_df = load_vix_futures_data()

# GUI
st.set_page_config(page_title="VolWo Dashboard", layout="wide")
st.title("📊 VolWo Dashboard")

tabs = st.tabs(["Dashboard", "VIX/VIX-Future"])

with tabs[0]:
    st.subheader("📈 Haupt-Dashboard")
    st.write("Hier kommen andere Charts, Signale, Tabellen etc.")

with tabs[1]:
    st.subheader("📉 VIX & VIX-Futures")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = plot_vix_term_structure(vix_futures_df)
        st.pyplot(fig1)
    with col2:
        fig2 = plot_vix_with_sma(vix_df)
        st.pyplot(fig2)
