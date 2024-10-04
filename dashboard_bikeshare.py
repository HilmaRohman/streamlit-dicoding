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

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

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

monthly_users_df = create_monthly_users_df(main_data)
weekday_users_df = create_weekday_users_df(main_data)
seasonly_users_df = create_seasonly_users_df(main_data)
hourly_users_df = create_hourly_users_df(main_data)
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
# fig = px.line(monthly_users_df,
#               x='yearmonth',
#               y=['casual_rides', 'registered_rides', 'total_rides'],
#               color_discrete_sequence=["skyblue", "orange", "red"],
#               markers=True,
#               title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

# st.plotly_chart(fig, use_container_width=True)

# fig1 = px.bar(seasonly_users_df,
            #   x='season',
            #   y=['count_rides'],
            #   color='type_of_rides',
            #   color_discrete_sequence=["skyblue", "orange", "red"],
            #   title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

#st.plotly_chart(fig, use_container_width=True)

# fig2 = px.bar(weekday_users_df,
#               x='weekday',
#               y=['count_rides'],
#               color='type_of_rides',
#               barmode='group',
#               color_discrete_sequence=["skyblue", "orange", "red"],
#               title='Count of bikeshare rides by weekday').update_layout(xaxis_title='', yaxis_title='Total Rides')

#st.plotly_chart(fig, use_container_width=True)

# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig1, use_container_width=True)
# right_column.plotly_chart(fig2, use_container_width=True)

# fig = px.line(hourly_users_df,
#               x='hr',
#               y=['casual_rides', 'registered_rides'],
#               color_discrete_sequence=["skyblue", "orange"],
#               markers=True,
#               title='Count of bikeshare rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

# st.plotly_chart(fig, use_container_width=True)

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
