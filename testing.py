import pandas as pd
import streamlit as st

st.title("🟣 Quick Column Checker")

uploaded_file = st.file_uploader("Upload your cost summary file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("✅ Columns in your Excel file:")
    st.write(df.columns.tolist())
