import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

# Using columns for a clean dashboard layout
col1, col2 = st.columns(2)

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

        # ---- ADDED INTERACTIVE SELECTBOX FOR STATE FILTERING ----
        if "State_ANSI" in df.columns:
            selected_state = st.selectbox("Select State", df["State_ANSI"].unique())
            filtered_df = df[df["State_ANSI"] == selected_state]
            
            # Show the filtered results in the dataframe view
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"Failed to load data: {e}")

with col2:
    st.subheader("📊 Milk Production Visualization")

    if "df" in locals() and "Value" in df.columns and "State_ANSI" in df.columns:
        # Sort data to get the absolute top producer for the metrics card
        df_sorted_desc = df.sort_values(by="Value", ascending=False)
        
        # ---- ADDED HIGH-LEVEL SUMMARY METRIC CARDS ----
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Top Producer", str(df_sorted_desc.iloc[0]["State_ANSI"]))
        with metric_col2:
            st.metric("Production", f'{df_sorted_desc.iloc[0]["Value"]:,.0f}')
            
        st.markdown("---")

        # Sort data ascending for a clean bottom-to-top layout on the horizontal bar chart
        df_sorted_asc = df.sort_values(by="Value", ascending=True)

        # Build a highly stable horizontal bar chart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Format numbers to Billions (e.g., 457B) on the x-axis
        def format_billion(x, pos):
            return f"{x*1e-9:.0f}B"
        
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(format_billion))

        # We map State_ANSI to the y-axis, and Value to the x-axis
        y_labels = df_sorted_asc["State_ANSI"].astype(str)
        ax.barh(y_labels, df_sorted_asc["Value"], color="#1f77b4", edgecolor="none")
        
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
        
        # ---- ADDED KEY INSIGHTS SECTION ----
        st.markdown("### 📈 Key Insight")
        st.write("California dominates U.S. milk production, contributing the largest share among all states.")
