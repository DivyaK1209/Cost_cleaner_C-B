import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Cost Summary Cleaner", layout="wide")
st.title("💼 Cost Summary Excel Cleaner")

uploaded_file = st.file_uploader("Upload your Cost Summary Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        col_map = {
            "DESCRIPTION": "DESCRIPTION",
            "Quantity": "Quantity",
            "Unit": "Unit",
            "Total": "Total"
        }
        df = df.rename(columns=col_map)

        # Assign categories from heading rows
        df["Category"] = None
        current_category = None
        for i, row in df.iterrows():
            if pd.isna(row["Quantity"]) and pd.isna(row["Unit"]) and pd.isna(row["Total"]):
                current_category = str(row["DESCRIPTION"]).strip()
                df.at[i, "Category"] = None
            else:
                df.at[i, "Category"] = current_category

        # Clean Unique_Description
        df["Unique_Description"] = df.apply(
        lambda x: x["DESCRIPTION"] if pd.isna(x["Category"]) else f"{x['DESCRIPTION']} - {x['Category']}",
        axis=1
)


        # Filter and reorder
        cleaned_df = df[["Unique_Description", "Quantity", "Unit", "Total", "Category"]]

        st.markdown("### Cleaned Data Preview")
        st.dataframe(cleaned_df, use_container_width=True)

        # ✅ Download section
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        output.seek(0)  # VERY IMPORTANT!

        st.download_button(
            label="📥 Download Cleaned Excel",
            data=output,
            file_name="Cleaned_Cost_Summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
