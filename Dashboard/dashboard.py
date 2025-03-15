# Melakukan import library yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Membuat dataframe yang dibutuhkan 
# Untuk mengetahui performa data pada pertanyaan 1 
def create_monthbikesharing1_df(df, year):
    # Proses untuk melakukan filter data berdasarkan tahun
    filteryear2_df = df[df["yr_x"] == year]
    monthbikesharing_df = filteryear2_df.groupby(by="mnth_x").agg({
        "casual_x": "sum",
        "registered_x": "sum",
        "cnt_x": "sum",
    }).reset_index()

    monthbikesharing_df = monthbikesharing_df.reset_index()
    
    return monthbikesharing_df

# Proses untuk membuat dataframe pada data hour
def create_byhour_df(df):
    filterhour_df = df[(df["mnth_y"] == 1) & (df["yr_y"] == 0)]
    byhour_df = filterhour_df.groupby(["hr", "mnth_y"]).agg({
        "casual_y": "sum",
        "registered_y": "sum",
        "cnt_y": "sum",
    }).reset_index()
   
    return byhour_df

all_df = pd.read_csv("main_data.csv")
 
#Proses membuat sidebar dengan menambahkan foto dan teks
with st.sidebar:
    st.image("bike-sharing.png")
    year = st.selectbox('Pilih Tahun Performa Sewa Sepeda:', ('2011', '2012'))
    st.write('Tahun:', year)

select_year = 0 if year == '2011' else 1

main_df = all_df

#Menyiapkan berbagai dataframe
day_df = create_monthbikesharing1_df(main_df, select_year)
hour_df = create_byhour_df(main_df)

#Membuat tulisan header dan subheader pada halaman dashboard
st.header('Bike Sharing Company')
st.subheader('Performa Sewa Sepeda')

#Melakukan proses pengelompokkan data berdasarkan bulan
day_sort_df=day_df.groupby(["mnth_x"]).agg({
    "cnt_x": "sum",
}).reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_sort_df["mnth_x"], 
    day_sort_df["cnt_x"], 
    label=f"Tahun {year}", 
    marker='o',
)

ax.set_title(f"Jumlah Pengguna berdasarkan Bulan Tahun {year}", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.legend()

st.pyplot(fig)

#Membuat visualisasi data menggunakan barplot
st.subheader("Nilai Terbanyak dan Terendah Sewa Sepeda")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="cnt_y", 
    x="hr",
    data=hour_df.sort_values(by="cnt_y", ascending=False),
    ax=ax
)
ax.set_title("Nilai Terbanyak dan Terendah Pengguna Sewa Sepeda Berdasarkan Jam Tahun 2011", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#Fungsi untuk menampilkan caption
st.caption('Copyright © Proyek Analisis 2025')