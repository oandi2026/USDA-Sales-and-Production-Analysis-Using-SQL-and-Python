import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Page configuration 
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

# Using columns for a clean dashboard layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📌 Project Overview")
    st.write(
        "This application analyzes U.S. agricultural production trends using public USDA datasets "
        "to provide supply chain insights and market segmentation."
    )

    st.subheader("🔍 Data Summary")
    # Reading the milk data file located in the data/ folder
    try:
        df = pd.read_csv("data/top_5_milk_producers.csv")
        df.columns = df.columns.str.strip()

        if "Value" in df.columns:
            df = df.rename(columns={"Value": "Total_Milk_Production"})

        if "State_Name" in df.columns:
            df = df.rename(columns={"State_Name": "State"})

        if "Total_Milk_Production" in df.columns:
            df["Total_Milk_Production"] = (
                df["Total_Milk_Production"]
                .astype(str)
                .str.replace(",", "")
                .astype(float)
            )

        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Failed to load data: {e}")

with col2:
    st.subheader("📊 Milk Production Visualization")

    if "df" in locals():

        df = df.sort_values(by="Total_Milk_Production", ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.set_theme(style="whitegrid")

        sns.barplot(
            x="Total_Milk_Production",
            y="State",       
            data=df,
            hue="State",       
            palette="Blues_r",
            legend=False,
            ax=ax,
        )

        ax.set_title(
            "Top U.S. Milk Producing States",
            fontsize=12,
            weight="bold",
        )

        plt.tight_layout()
        st.pyplot(fig)

else:
    st.warning("Required columns not found in dataset.")


