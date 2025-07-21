# Build Streamlit dashboard

# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("NBA Player Stats Dashboard")

df = pd.read_csv("data/nba_stats.csv")
player = st.selectbox("Choose player", df['Player'].unique())
chart = px.line(df[df['Player'] == player], x='Game', y='Points', title=f'{player} - Points Over Time')
st.plotly_chart(chart)
