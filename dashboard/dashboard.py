import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup Konfigurasi Streamlit (Harus Paling Atas)
st.set_page_config(page_title="E-Commerce Analytics", page_icon="🛍️", layout="wide")

sns.set(style='ticks')

# --- Helper functions ---
@st.cache_data
def load_data():
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    all_df = pd.read_csv(os.path.join(current_dir, "main_data.csv"))
    rfm_df = pd.read_csv(os.path.join(current_dir, "rfm_data.csv"))
    
    if "order_purchase_timestamp" in all_df.columns:
        all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])
    return all_df, rfm_df

try:
    all_df, rfm_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# --- Custom CSS untuk Estetika ---
st.markdown("""
<style>
    .metric-card {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR INTERACTIVE FILTER ---

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/263/263142.png", width=80)
st.sidebar.title("E-Commerce Analytics")

min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

start_date, end_date = st.sidebar.date_input(
    label='Saring Rentang Waktu Pesanan',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Tentang Dashboard Lanjutan Ini")
st.sidebar.info("Dashboard ini kini tidak lagi berstruktur dasar. Mengandung sistem navigasi *Tab*, Filter Waktu Interaktif, Kartu Metrik dengan Tooltip, serta Analisis Demografi Geografis Ekstensi berdasarkan permintaan untuk kompleksitas tertinggi.")

# Filter Engine Berdasarkan Kalender Input Sidebar
filtered_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                     (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# --- MAIN TITLE & HEADER ---
st.title('🛍️ Dashboard Analisis E-Commerce Canggih')
st.markdown("Eksplorasi wawasan performa penjualan secara mendalam melalui berbagai lensa pandang metriks profesional.")

# --- TABS LAYOUT SYSTEM ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Ringkasan Penjualan", "📦 Performa Barisan Produk", "👥 Kecerdasan Segmentasi (RFM)", "🗺️ Demografi Pelanggan"])

# ================= TAB 1: EXECUTIVE SUMMARY =================
with tab1:
    st.markdown("### Matriks Performa Bisnis Utama")
    
    # 4 Kolom Metrik
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Order Sukses", value=f"{filtered_df.order_id.nunique():,}")
    with col2:
        st.metric("Estimasi Total Pendapatan", value=f"R$ {filtered_df.price.sum():,.0f}")
    with col3:
        avg_value = filtered_df.price.sum() / filtered_df.order_id.nunique() if filtered_df.order_id.nunique() > 0 else 0
        st.metric("Rerata Nilai per Pesanan", value=f"R$ {avg_value:,.2f}")
    with col4:
        st.metric("Total Konsumen Aktif", value=f"{filtered_df.customer_id.nunique():,}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Laju Dinamika Trend (Bulanan)")
    monthly_trend = filtered_df.resample(rule='ME', on='order_purchase_timestamp').agg({"order_id": "nunique", "price": "sum"}).reset_index()
    monthly_trend.rename(columns={"order_purchase_timestamp": "Bulan", "order_id": "Jumlah Pesanan", "price": "Pendapatan"}, inplace=True)
    monthly_trend["Bulan"] = monthly_trend["Bulan"].dt.strftime('%Y-%m')
    
    # Dua grafik trend paralel bersandingan agar kompleks
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="Bulan", y="Jumlah Pesanan", data=monthly_trend, marker='o', color="#1f77b4", linewidth=2.5, ax=ax1)
        ax1.set_title("Volatilitas Jumlah Pesanan per Bulan", fontsize=15, fontweight='bold', pad=15)
        ax1.tick_params(axis='x', rotation=45)
        sns.despine(trim=True) # Trim spine untuk lebih estetik
        st.pyplot(fig1)
        
    with fig_col2:
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="Bulan", y="Pendapatan", data=monthly_trend, marker='s', color="#ff7f0e", linewidth=2.5, ax=ax2)
        ax2.set_title("Trajektori Pendapatan Finansial (BRL R$)", fontsize=15, fontweight='bold', pad=15)
        ax2.tick_params(axis='x', rotation=45)
        sns.despine(trim=True)
        st.pyplot(fig2)

# ================= TAB 2: PRODUCT DEEP-DIVE =================
with tab2:
    st.markdown("### Lanskap Daya Tarik & Dominasi Produk")
    
    sum_items = filtered_df.groupby("product_category_name_english").order_item_id.count().sort_values(ascending=False).reset_index()
    sum_items.rename(columns={"order_item_id": "Terjual"}, inplace=True)
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.success("🏆 10 Lini Kategori Terlaris (Top Performers)")
        fig, ax = plt.subplots(figsize=(8, 8))
        sns.barplot(x="Terjual", y="product_category_name_english", data=sum_items.head(10), palette="Blues_d", ax=ax)
        ax.set_ylabel(None); ax.set_xlabel("Volume Unit Terjual")
        for i, v in enumerate(sum_items.head(10)["Terjual"]):
            ax.text(v + 50, i + 0.15, str(v), color='black', fontsize=11, fontweight='bold')
        sns.despine(right=True, top=True)
        st.pyplot(fig)
        
    with viz_col2:
        st.error("🚨 10 Lini Kategori Kurang Peminat (Underperforming)")
        fig, ax = plt.subplots(figsize=(8, 8))
        sns.barplot(x="Terjual", y="product_category_name_english", data=sum_items.tail(10).sort_values(by="Terjual", ascending=True), palette="Reds_d", ax=ax)
        ax.set_ylabel(None); ax.set_xlabel("Volume Unit Terjual")
        ax.invert_xaxis()
        ax.yaxis.set_label_position("right"); ax.yaxis.tick_right()
        for i, v in enumerate(sum_items.tail(10).sort_values(by="Terjual", ascending=True)["Terjual"]):
            ax.text(v + 0.1, i + 0.15, str(v), color='#b30000', fontsize=11, fontweight='bold', ha='left')
        sns.despine(left=True, right=False, top=True)
        st.pyplot(fig)

# ================= TAB 3: RFM SEGMENTATION =================
with tab3:
    st.markdown("### Kecerdasan Ekstraktif (Model Klasifikasi Manual RFM)")
    
    # Tooltip metrics UI
    st.markdown("Laporan matrik pembobotan skor perilaku *(Behavioral Scoring)* pelanggan dalam siklus hidup komersilnya.")
    metric_c1, metric_c2, metric_c3 = st.columns(3)
    metric_c1.metric("Rerata Keterkinian (Recency)", f"{round(rfm_df.recency.mean(), 1)} Hari", help="Jeda temporal rata-rata (dalam hitungan hari) sejak konsumen melakukan check-out terakhir mereka di platform.")
    metric_c2.metric("Rerata Frekuensi Tular", f"{round(rfm_df.frequency.mean(), 2)} Kali", help="Rata-rata seberapa intens pelanggan melakukan transaksi pemesanan ganda di lapak.")
    metric_c3.metric("Rata-rata Moneter Bruto", f"R$ {round(rfm_df.monetary.mean(), 2)}", help="Rata-rata total uang riil yang dikeluarkan tiap satu pelanggan tunggal kepada Olist.")
    
    st.markdown("---")
    
    # Kombinasi Bar Plot + Data Table
    clust_col1, clust_col2 = st.columns([2, 1.3])
    with clust_col1:
        st.markdown("#### Proporsi Pangsa Segmen Pelanggan")
        segment_counts = rfm_df['customer_segment'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6.5))
        sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="mako", ax=ax)
        ax.set_ylabel("Total Entitas Bersangkutan", fontsize=12)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=10, rotation=15)
        for i, v in enumerate(segment_counts.values):
            ax.text(i, v + int(segment_counts.values.max()*0.02), f"{v:,}", ha='center', color='black', fontsize=11, fontweight='bold')
        sns.despine()
        st.pyplot(fig)
        
    with clust_col2:
        st.markdown("#### Katalog 'Pelanggan Prioritas'")
        st.caption("Basis tabular ini memuat sampel profil-profil dengan kontribusi pengeluaran paling bernilai tinggi (Raja Pemasukan).")
        # Menampilkan Dataframe yang di highlight
        top_cutomers = rfm_df[rfm_df['customer_segment'] == "Pelanggan Prioritas"].sort_values(by="monetary", ascending=False).head(15)
        
        # Style dataframe mapping
        styled_df = top_cutomers[['customer_unique_id', 'recency', 'monetary']].reset_index(drop=True)
        styled_df.columns = ["ID Akun Abstrak", "Recency (Hr)", "Income (R$)"]
        st.dataframe(styled_df, use_container_width=True, height=400)

# ================= TAB 4: GEOGRAPHIC IMPACT =================
with tab4:
    st.markdown("### Relasi Peta Demografis Terhadap Densitas Permintaan")
    
    if "customer_state" in filtered_df.columns:
        state_counts = filtered_df.groupby('customer_state').customer_id.nunique().sort_values(ascending=False).reset_index()
        state_counts.rename(columns={'customer_id': 'Total Populasi Aktif'}, inplace=True)
        
        st.markdown("#### 10 Basis Negara Bagian Geografis Terpadat (Traffic Tertinggi)")
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.barplot(x='customer_state', y='Total Populasi Aktif', data=state_counts.head(10), palette='viridis', ax=ax)
        for i, v in enumerate(state_counts.head(10)['Total Populasi Aktif']):
            ax.text(i, v + int(state_counts.head(10)['Total Populasi Aktif'].max()*0.02), f"{v:,}", ha='center', fontweight='bold', fontsize=12)
        ax.set_xlabel("Singkatan Negara Bagian Geografis (State Acronym)", fontsize=13)
        ax.set_ylabel("Volume Trafik Konsumen", fontsize=13)
        sns.despine(trim=True)
        st.pyplot(fig)
        
        # Expander tersembunyi untuk melengkapi kerumitan tanpa mengotori ruang
        with st.expander("Buka Raw Data Distribusi Ratusan Kota (Drill-Down)"):
            st.info("Anda bisa menyortir dan menelusuri data interaktif di bawah ini untuk melihat metrik kepadatan pembeli spesifik ke tingkatan nama Kota asli.")
            city_counts = filtered_df.groupby('customer_city').agg({
                'customer_id': 'nunique',
                'price': 'sum'
            }).sort_values(by='customer_id', ascending=False).reset_index()
            city_counts.rename(columns={'customer_city': 'Nama Kota (City Name)', 'customer_id': 'Densitas Pengguna', 'price': 'Total Transaksi Masuk (R$)'}, inplace=True)
            st.dataframe(city_counts, use_container_width=True)
    else:
        st.warning("Data demografi geografis tidak terdeteksi pada skema dataset rentang ini.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Submission &copy; Sahrul Firdaus 2023</p>", unsafe_allow_html=True)
