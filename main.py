import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from millify import millify

# Make most out of the space available
st.set_page_config(layout="wide")
# Matplotlib styling
plt.style.use("ggplot")

# Open dataset as a pandas dataframe
df = pd.read_csv(
    "./SeoulBikeData.csv",
    encoding="unicode_escape",
    parse_dates=["Date"],
    date_format="%d/%m/%Y",
)

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
    st.bar_chart(df, x="Temperature(°C)", y="Rented Bike Count", height=550)

with col22:
    fig, ax = plt.subplots()
    ax.pie([35, 25, 25, 15])
    st.pyplot(fig, transparent=True)
