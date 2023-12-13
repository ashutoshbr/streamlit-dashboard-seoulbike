import altair as alt
import pandas as pd
import streamlit as st
from millify import millify

# Make most out of the space available
st.set_page_config(layout="wide")

# Open dataset as a pandas dataframe
df = pd.read_csv(
    "./SeoulBikeData.csv",
    encoding="unicode_escape",
    parse_dates=["Date"],
    date_format="%d/%m/%Y",
)


def normalize_column(col) -> None:
    max_value = df[col].max()
    df["Normalized" + " " + col] = df[col].div(max_value)


# The first container with two metrics and a line chart
container1 = st.container()
col11, col12 = container1.columns([0.15, 0.85])
with col11:
    total_rented_bikes = df["Rented Bike Count"].sum()
    hours_ridden = df["Hour"].sum()
    st.metric(
        label="Total Bikes Rented", value=millify(total_rented_bikes, precision=2)
    )
    st.metric(label="Hours Ridden", value=millify(hours_ridden, precision=2))
with col12:
    st.line_chart(df, x="Date", y="Rented Bike Count")

# The second container with a bar chart & a pie chart
container2 = st.container(border=True)
col21, col22 = container2.columns([0.6, 0.4])
with col21:
    st.bar_chart(df, x="Seasons", y="Rented Bike Count")

with col22:
    grp_by_seasons = df.groupby("Seasons")["Rented Bike Count"].sum()
    grp_by_seasons = grp_by_seasons.reset_index()
    print(grp_by_seasons)
    ac = (
        alt.Chart(grp_by_seasons)
        .mark_arc()
        .encode(
            theta="Rented Bike Count",
            color="Seasons",
        )
    )
    st.altair_chart(ac)

# The third container with a scatter plot
container3 = st.container(border=True)
with container3:
    normalize_column("Rainfall(mm)")
    normalize_column("Snowfall (cm)")
    bubble_size = st.slider("Bubble Size", 0, 200, 50)
    st.scatter_chart(
        df,
        x="Rented Bike Count",
        y=["Normalized Rainfall(mm)", "Normalized Snowfall (cm)"],
        size=bubble_size,
        color=["#348abd", "#e24a33"],
    )

# Fourth container with a bar chart and a scatter plot
container4 = st.container(border=True)
col41, col42, col43 = container4.columns([0.33, 0.33, 0.33])
with col41:
    st.bar_chart(df, x="Holiday", y="Rented Bike Count")
with col42:
    st.scatter_chart(
        df,
        x="Wind speed (m/s)",
        y="Rented Bike Count",
    )
with col43:
    st.scatter_chart(
        df,
        x="Solar Radiation (MJ/m2)",
        y="Rented Bike Count",
    )

# Bubble plot
container5 = st.container(border=True)
with container5:
    ac = (
        alt.Chart(df, height=600)
        .mark_point()
        .encode(x="Temperature(°C)", y="Rented Bike Count", size="Hour")
    )
    st.altair_chart(ac, use_container_width=True)
