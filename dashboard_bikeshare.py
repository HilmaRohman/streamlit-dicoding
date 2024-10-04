import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Memasukkan dataset

df = pd.read_csv("https://raw.githubusercontent.com/HilmaRohman/dicoding-data/refs/heads/main/cleaned_dataset.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Dashboard Bikeshare",
                   layout="wide")

# Membuat fungsi yang mengatur data

def create_byseason_df(df):
    byseason_df = df.groupby('season')['cnt'].sum().reset_index()
    return byseason_df

# membuat rentang waktu

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# sidebar
with st.sidebar:
    # menambahkan logo
    st.image("https://raw.githubusercontent.com/HilmaRohman/dicoding-data/refs/heads/main/bikeshare.png")
    st.sidebar.header("Rentang waktu:")
    # mMengambil waktu awal & waktu akhir
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# hubungkan filter dengan main_data
main_data = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]
# memanggil fungsi sebelumnya
bysession_df = create_byseason_df(main_data)
# Menu utama
st.title("Bikesharing dashboard")
st.markdown("##")
col1, col2 = st.columns(2)
with col1:
    jumlah_casual = main_data['casual'].sum()
    st.metric("Jumlah Pengendara Casual", value=jumlah_casual)
with col2:
    jumlah_registrasi = main_data['registered'].sum()
    st.metric("Jumlah Pengendara Registered", value=jumlah_registrasi)

st.markdown("---")
# Grafik
# barplot
fig, ax = plt.subplots(figsize=(17, 8))
sns.barplot(
        y="cnt", 
        x="season",
        data=bysession_df.sort_values(by="season", ascending=False),
        ax=ax,
        color="red"
)
ax.set_title("Jumlah Pengguna Bikeshare tiap musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
# scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_data, x="atemp", y="cnt", hue="holiday", ax=ax,palette={0: "black", 1: "red"})
ax.set_title("Jumlah pengguna bikshare berdasarkan liburan dan suhu", fontsize=20)
ax.set_xlabel("Temperature (atemp)", fontsize=14)
ax.set_ylabel("Count (cnt)", fontsize=14)
st.pyplot(fig)
# footer
st.caption('Dibuat oleh M. Hilma Minanur Rohman')
# Menghilangkan streamlit style
hide= """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide, unsafe_allow_html=True)
