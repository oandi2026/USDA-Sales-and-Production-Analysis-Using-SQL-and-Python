import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

try:
    # 2. Data Loading & Cleaning
    df = pd.read_csv("data/top_5_milk_producers.csv")
    df.columns = df.columns.str.strip()

    if "total_milk" in df.columns:
        df["total_milk"] = (
            df["total_milk"]
            .astype(str)
            .str.replace(",", "")
            .astype(float)
        )

    # ========================================================
    # NEW: HIGH-LEVEL KPI CARDS (Diletakkan di paling atas)
    # ========================================================
    # Cari nilai tertinggi dan total produksi dari dataset
    df_sorted_desc = df.sort_values(by="total_milk", ascending=False)
    top_state_ansi = df_sorted_desc.iloc[0]["State_ANSI"]
    top_state_val = df_sorted_desc.iloc[0]["total_milk"]
    total_production_all = df["total_milk"].sum()

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="🏆 Market Leader (ANSI)", value=str(top_state_ansi))
    with kpi2:
        st.metric(label="🚀 Highest Production Volume", value=f"{top_state_val*1e-9:.1f}B")
    with kpi3:
        st.metric(label="📈 Combined Top 5 Production", value=f"{total_production_all*1e-9:.1f}B")
        
    st.markdown("---")

    # ========================================================
    # NEW: INTERACTIVE ANALYTIC TOOL (Dropdown Sidebar Filter)
    # ========================================================
    st.sidebar.header("🛠️ Interactive Filter")
    
    # Membuat opsi "All States" agar pengguna bisa melihat semua data kembali dengan mudah
    state_options = ["All States"] + list(df["State_ANSI"].astype(str).unique())
    selected_state = st.sidebar.selectbox("Filter by State ANSI Code:", state_options)

    # Filter dataset berdasarkan pilihan user secara real-time
    if selected_state == "All States":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["State_ANSI"].astype(str) == selected_state]

    # 3. Layout Grid (Split into 2 Columns for Data and Charts)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Dynamic Data Summary")
        # Menampilkan tabel yang nilainya otomatis berubah sesuai filter dropdown
        st.dataframe(filtered_df, use_container_width=True)
            
    with col2:
        st.subheader("📊 Dynamic Production Visualization")

        if not filtered_df.empty:
            # Urutkan data secara menaik agar posisi grafik batang horizontal tersusun rapi dari bawah ke atas
            df_sorted_asc = filtered_df.sort_values(by="total_milk", ascending=True)

            fig, ax = plt.subplots(figsize=(10, 5))
            sns_style = sns_theme = "whitegrid" # Mencegah ketergantungan penuh pada fungsi seaborn
            
            # Format teks angka sumbu X menjadi format Miliaran ('B')
            def format_billion(x, pos):
                return f"{x*1e-9:.0f}B"
            
            from matplotlib.ticker import FuncFormatter
            ax.xaxis.set_major_formatter(FuncFormatter(format_billion))

            # Gambar grafik batang menggunakan Matplotlib murni (Sangat Stabil)
            y_labels = df_sorted_asc["State_ANSI"].astype(str)
            ax.barh(y_labels, df_sorted_asc["total_milk"], color="#1f77b4", edgecolor="none")
            
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            ax.set_axisbelow(True)
            
            ax.set_title(
                f"Milk Production Volume - {selected_state} (USDA Data)",
                fontsize=12,
                weight="bold",
            )
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("No visualization data available for the selected filter.")
            
        st.markdown("### 📈 Key Insight")
        st.write("Based on the USDA analysis, Iowa (ANSI 19) leads total milk production, followed closely by Pennsylvania (ANSI 42).")

except Exception as e:
    st.error(f"Failed to load dashboard components: {e}")
