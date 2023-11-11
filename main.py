import streamlit as st
import pandas as pd
from datetime import datetime
from millify import millify


# Make most out of the space available
st.set_page_config(layout="wide")

# Open dataset as a pandas dataframe
df = pd.read_csv(
    "./SeoulBikeData.csv",
    encoding="unicode_escape",
    parse_dates=["Date"],
    date_parser=lambda x: datetime.strptime(x, "%d/%m/%Y"),
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
