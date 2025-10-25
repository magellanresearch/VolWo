import streamlit as st
import pandas as pd
import os

def show_database():
    st.subheader("🗂️ VolWo Database")

    # Example: Load CSV files from a local 'database' folder
    data_files = [f for f in os.listdir("database") if f.endswith(".csv")]

    if not data_files:
        st.warning("No data files found in the database folder.")
        return

    selected_file = st.selectbox("Choose a dataset", data_files)
    df = pd.read_csv(os.path.join("database", selected_file))

    st.write(f"Preview of `{selected_file}`:")
    st.dataframe(df)

    # Optional: Add summary stats
    if st.checkbox("Show summary statistics"):
        st.write(df.describe())
