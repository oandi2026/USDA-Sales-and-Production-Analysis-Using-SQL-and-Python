import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

# Using columns for a clean dashboard layout
col1, col2 = st.columns()

with col1:
    st.subheader("📌 Project Overview")
    st.write(
        "This application analyzes U.S. agricultural production trends using public USDA datasets "
        "to provide supply chain insights and market segmentation."
    )

    st.subheader("🔍 Data Summary")
    
    try:
        # Load data and strip any hidden spaces from column names
        df = pd.read_csv("data/top_5_milk_producers.csv")
        df.columns = df.columns.str.strip()

        # Clean the 'Value' column numbers into decimals/floats
        if "Value" in df.columns:
            df["Value"] = (
                df["Value"]
                .astype(str)
                .str.replace(",", "")
                .astype(float)
            )

        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load data: {e}")

with col2:
    st.subheader("📊 Milk Production Visualization")

    if "df" in locals() and "Value" in df.columns and "State_ANSI" in df.columns:
        # Sort data so the highest producer is at the top
        df = df.sort_values(by="Value", ascending=True)

        # Build a highly stable horizontal bar chart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Format numbers to Billions (e.g., 457B) on the x-axis
        def format_billion(x, pos):
            return f"{x*1e-9:.0f}B"
        
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(format_billion))

        # We map State_ANSI to the y-axis, and Value to the x-axis
        # Convert State_ANSI to string so it is treated as a clean label on the chart
        y_labels = df["State_ANSI"].astype(str)
        
        ax.barh(y_labels, df["Value"], color="#1f77b4", edgecolor="none")
        
        # Grid layout
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        
        ax.set_title(
            "Top 5 U.S. Milk Producing States by ANSI Code (USDA Data)",
            fontsize=12,
            weight="bold",
        )
        
        plt.tight_layout()
        st.pyplot(fig)
