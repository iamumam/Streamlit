import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
df_hour = pd.read_csv('all_data.csv')
df_day = pd.read_csv('all_data.csv')

# Set the Streamlit page layout
st.set_page_config(layout="wide", page_title="Dashboard Analisis Penggunaan Sepeda")

# Title of the Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")

# Sidebar
st.sidebar.header("Pengaturan Visualisasi")
show_by_time = st.sidebar.checkbox("Tampilkan Total Peminjaman Berdasarkan Jam", True)
show_by_day = st.sidebar.checkbox("Tampilkan Rata-rata Penggunaan: Hari Kerja vs Akhir Pekan", True)
show_by_time_category = st.sidebar.checkbox("Tampilkan Total Peminjaman Berdasarkan Kategori Waktu", True)

# Main body of the dashboard
st.markdown("## Analisis Penggunaan Sepeda")

# 1. Visualisasi Total Peminjaman Sepeda Berdasarkan Jam
if show_by_time:
    st.markdown("### Total Peminjaman Sepeda Berdasarkan Jam")
    hourly_usage = df_hour.groupby('hr')['cnt'].sum()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=hourly_usage.index, y=hourly_usage.values, palette="plasma")
    
    plt.title('Total Peminjaman Sepeda Berdasarkan Jam', fontsize=16)
    plt.xlabel('Jam', fontsize=12)
    plt.ylabel('Total Peminjaman Sepeda (cnt)', fontsize=12)
    plt.xticks(ticks=range(0, 24))
    
    # Tampilkan plot di Streamlit
    st.pyplot(plt)

# 2. Visualisasi Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan
if show_by_day:
    st.markdown("### Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan")
    weekday_usage = df_day.groupby('weekday')['cnt'].mean().reset_index()
    weekday_usage['day_type'] = weekday_usage['weekday'].apply(lambda x: 'Akhir Pekan' if x >= 5 else 'Hari Kerja')
    
    day_type_usage = weekday_usage.groupby('day_type')['cnt'].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.barplot(x='day_type', y='cnt', data=day_type_usage, palette="Set2")

    plt.title('Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan', fontsize=16)
    plt.xlabel('Tipe Hari', fontsize=12)
    plt.ylabel('Rata-rata Pengguna Sepeda (cnt)', fontsize=12)
    
    # Tampilkan plot di Streamlit
    st.pyplot(plt)

# 3. Visualisasi Total Peminjaman Sepeda Berdasarkan Kategori Waktu
if show_by_time_category:
    st.markdown("### Total Peminjaman Sepeda Berdasarkan Kategori Waktu")
    
    def categorize_time(hr):
        if hr < 6:
            return 'Early Morning'
        elif 6 <= hr < 12:
            return 'Morning'
        elif 12 <= hr < 18:
            return 'Afternoon'
        else:
            return 'Evening'

    df_hour['Time Category'] = df_hour['hr'].apply(categorize_time)
    time_grouped_data = df_hour.groupby('Time Category').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=time_grouped_data,
                x='Time Category',
                y='cnt',
                palette='viridis',
                ci=None)

    plt.title('Total Peminjaman Sepeda Berdasarkan Kategori Waktu', fontsize=16)
    plt.xlabel('Kategori Waktu', fontsize=12)
    plt.ylabel('Total Peminjaman (cnt)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

# Footer
st.markdown("### Kesimpulan")
st.markdown("""
- **Waktu Puncak Penggunaan Sepeda:** Puncak penggunaan sepeda terjadi pada jam 18 atau sore hari.
- **Pengaruh Hari Kerja:** Tidak ditemukan perbedaan signifikan antara penggunaan sepeda pada hari kerja dan akhir pekan.
- **Kategori Waktu:** Penggunaan sepeda paling banyak terjadi di sore hari ('Afternoon').
""")
