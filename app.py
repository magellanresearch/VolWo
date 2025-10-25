import streamlit as st
from modules.data_loader import fetch_recent_data, fetch_full_history
from modules.plotting import plot_vix, plot_etps, plot_strategies, plot_vix_term_structure
from modules.analysis import analyze_data
from modules.database import show_database

# Set page config
st.set_page_config(page_title="VolWo Dashboard", layout="wide")

# Sidebar menu
menu = st.sidebar.radio("Navigation", [
    "Dashboard",
    "VIX/VIX-Future",
    "Volatility-ETPS",
    "Volatility Strategies",
    "Data Analyzer",
    "Database",
    "University"
])

# Routing logic
if menu == "Dashboard":
    st.title("📊 VolWo Dashboard")
    
    # Show VIX Term Structure plot directly on dashboarddef set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://raw.githubusercontent.com/magellanresearch/VolWo/main/backvola.jpg")
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            opacity: 0.8;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    plot_vix_term_structure()

elif menu == "VIX/VIX-Future":
    st.title("📈 VIX and VIX Futures")
    plot_vix()

elif menu == "Volatility-ETPS":
    st.title("📉 Volatility ETPs")
    plot_etps()

elif menu == "Volatility Strategies":
    st.title("🧠 Volatility Strategies")
    plot_strategies()

elif menu == "Data Analyzer":
    st.title("🔍 Data Analyzer")
    analyze_data()

elif menu == "Database":
    st.title("🗂️ Database")
    show_database()

elif menu == "University":
    st.title("🎓 VolWo University")
    show_university()
