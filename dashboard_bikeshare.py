import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset

df = pd.read_csv("https://raw.githubusercontent.com/HilmaRohman/dicoding-data/refs/heads/main/cleaned_dataset.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Dashboard Bikeshare",
                   page_icon="bar_chart:",
                   layout="wide")

# create helper functions

def create_byseason_df(df):
    byseason_df = df.groupby('season')['cnt'].sum().reset_index()
    # bygender_df.rename(columns={
    #     "customer_id": "customer_count"
    # }, inplace=True)
    
    return byseason_df

# make filter components (komponen filter)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/HilmaRohman/dicoding-data/refs/heads/main/bikeshare.png")

    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
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

# assign main_data ke helper functions yang telah dibuat sebelumnya

bysession_df = create_byseason_df(main_data)

# ----- MAINPAGE -----
st.title(":bar_chart: Capital Bikeshare: Bike-Sharing Dashboard")
st.markdown("##")

col1, col2 = st.columns(2)

with col1:
    jumlah_casual = main_data['casual'].sum()
    st.metric("Jumlah Pengendara Casual", value=jumlah_casual)
with col2:
    jumlah_registrasi = main_data['registered'].sum()
    st.metric("Jumlah Pengendara Teregistrasi", value=jumlah_registrasi)

st.markdown("---")


# ----- CHART -----
fig, ax = plt.subplots(figsize=(25, 8))
sns.barplot(
        y="cnt", 
        x="season",
        data=bysession_df.sort_values(by="season", ascending=False),
        ax=ax
)



ax.set_title("Number of Customer by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


# -----[]

# Membuat scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_data, x="atemp", y="cnt", hue="holiday", ax=ax)

# Menambahkan judul dan pengaturan sumbu
ax.set_title("Scatter Plot of Count vs. Temperature with Holidays", fontsize=20)
ax.set_xlabel("Temperature (atemp)", fontsize=14)
ax.set_ylabel("Count (cnt)", fontsize=14)

# Menampilkan plot di aplikasi Streamlit
st.pyplot(fig)

# -----[]

st.caption('Dibuat oleh M. Hilma Minanur Rohman')

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
