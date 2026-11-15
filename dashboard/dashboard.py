from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# ---------- Konfigurasi halaman ----------
st.set_page_config(page_title="Bike Sharing Dashboard",
                   page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid")

# ---------- Load data ----------
BASE = Path(__file__).parent


@st.cache_data
def load_data():
    day = pd.read_csv(BASE / "main_data.csv", parse_dates=["dteday"])
    hour = pd.read_csv(BASE / "hour_clean.csv", parse_dates=["dteday"])
    return day, hour


day_df, hour_df = load_data()

# ---------- Sidebar: filter ----------
st.sidebar.header("🔎 Filter Data")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) != 2:
    st.info("Pilih tanggal akhir pada filter di sidebar.")
    st.stop()

start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

season_options = ["Spring", "Summer", "Fall", "Winter"]
selected_seasons = st.sidebar.multiselect(
    "Musim", season_options, default=season_options)

day_f = day_df[
    (day_df["dteday"] >= start)
    & (day_df["dteday"] <= end)
    & (day_df["season"].isin(selected_seasons))
]
hour_f = hour_df[
    (hour_df["dteday"] >= start)
    & (hour_df["dteday"] <= end)
    & (hour_df["season"].isin(selected_seasons))
]

if day_f.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ---------- Header & KPI ----------
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penyewaan sepeda 2011-2012 | Moh Reza")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Penyewaan", f"{day_f['cnt'].sum():,}")
c2.metric("Rata-rata per Hari", f"{day_f['cnt'].mean():,.0f}")
c3.metric("Pengguna Registered", f"{day_f['registered'].sum():,}")
c4.metric("Pengguna Casual", f"{day_f['casual'].sum():,}")

st.divider()

# ---------- Tab ----------
tab1, tab2, tab3 = st.tabs(
    ["Pertanyaan 1: Tren Bulanan",
     "Pertanyaan 2: Pola per Jam", "Analisis Lanjutan"]
)

# ===== Tab 1 =====
with tab1:
    st.subheader("Total Penyewaan Sepeda per Bulan")
    monthly = day_f.resample("ME", on="dteday")["cnt"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly, x="dteday", y="cnt", marker="o", ax=ax)
    ax.set_title("Total Penyewaan Sepeda per Bulan", fontsize=14)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Penyewaan")
    plt.tight_layout()
    st.pyplot(fig)

    top = monthly.loc[monthly["cnt"].idxmax()]
    low = monthly.loc[monthly["cnt"].idxmin()]
    col_a, col_b = st.columns(2)
    col_a.metric("Bulan Tertinggi", top["dteday"].strftime(
        "%b %Y"), f"{int(top['cnt']):,}")
    col_b.metric("Bulan Terendah", low["dteday"].strftime(
        "%b %Y"), f"{int(low['cnt']):,}")

    st.markdown(
        "**Insight:** Penyewaan mengikuti pola musiman, naik di bulan hangat "
        "dan turun di bulan dingin. Seluruh bulan di 2012 lebih tinggi daripada "
        "bulan yang sama di 2011, sehingga tren jangka panjangnya tumbuh."
    )

    st.divider()
    st.subheader("Kesimpulan & Rekomendasi (Pertanyaan 1: Tren Bulanan)")
    st.markdown("""
- **Kesimpulan 1:** Penyewaan tertinggi terjadi pada September 2012 (218.573) dan terendah pada Januari 2011 (38.189).
- **Kesimpulan 2:** Total penyewaan 2012 naik 64,9% dibanding 2011, dengan permintaan tertinggi pada Juli-September dan terendah pada Januari-Maret.
- **Rekomendasi:** Jadwalkan perawatan armada massal di bulan dingin dan siapkan stok penuh sebelum Juli-September.
""")
    st.caption(
        "Catatan: kesimpulan berlaku untuk seluruh periode 2011-2012, bukan hasil filter.")

# ===== Tab 2 =====
with tab2:
    st.subheader("Rata-rata Penyewaan per Jam: Hari Kerja vs Akhir Pekan")
    hourly = hour_f.groupby(["hr", "day_type"])["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=hourly, x="hr", y="cnt",
                 hue="day_type", marker="o", ax=ax)
    ax.set_title("Rata-rata Penyewaan per Jam", fontsize=14)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(0, 24))
    ax.legend(title="Tipe Hari")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(
        "**Insight:** Hari kerja memiliki dua puncak tajam di pagi dan sore hari "
        "(pola komuter), sedangkan akhir pekan naik perlahan dan memuncak di siang hari "
        "(pola rekreasi)."
    )

    st.divider()
    st.subheader("Kesimpulan & Rekomendasi (Pertanyaan 2: Pola per Jam)")
    st.markdown("""
- **Kesimpulan 1:** Hari kerja berpola komuter, dengan puncak di jam 8 (±477) dan jam 17-18 (tertinggi ±525 di jam 17).
- **Kesimpulan 2:** Akhir pekan berpola rekreasi, dengan puncak di jam 12-14 (±365-373) dan tanpa lonjakan pagi.
- **Rekomendasi:** Tambah ketersediaan sepeda di area perkantoran pada jam 07-09 dan 16-19 hari kerja, dan geser armada ke area wisata pada jam 11-15 di akhir pekan.
""")
    st.caption(
        "Catatan: kesimpulan berlaku untuk seluruh periode 2011-2012, bukan hasil filter.")

# ===== Tab 3 =====
with tab3:
    st.subheader("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
    temp_df = day_f.copy()
    temp_df["temp_category"] = pd.cut(
        temp_df["temp_c"], bins=[0, 15, 25, 50], labels=["Dingin", "Sedang", "Panas"]
    )
    temp_avg = temp_df.groupby("temp_category", observed=True)[
        "cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=temp_avg, x="temp_category", y="cnt", ax=ax)
    ax.set_title("Rata-rata Penyewaan per Kategori Suhu", fontsize=14)
    ax.set_xlabel("Kategori Suhu (Dingin <15°C, Sedang 15-25°C, Panas >25°C)")
    ax.set_ylabel("Rata-rata Penyewaan Harian")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(
        "**Insight:** Penyewaan naik seiring suhu. Lonjakan terbesar terjadi dari "
        "kategori Dingin ke Sedang, sedangkan dari Sedang ke Panas kenaikannya lebih landai."
    )

    st.divider()
    st.subheader("Kesimpulan & Rekomendasi (Analisis Lanjutan)")
    st.markdown("""
- **Kesimpulan 1:** Rata-rata penyewaan harian pada hari Dingin (±2.833) kira-kira separuh dari hari Panas (±5.632).
- **Kesimpulan 2:** Spring didominasi hari berpermintaan rendah (140 dari 181 hari), sedangkan Fall paling sering berpermintaan tinggi (96 dari 188 hari).
- **Rekomendasi:** Berikan promo atau insentif pada hari bersuhu dingin, dan siapkan armada maksimal saat musim Fall serta suhu hangat.
""")
    st.caption(
        "Catatan: kesimpulan berlaku untuk seluruh periode 2011-2012, bukan hasil filter.")
