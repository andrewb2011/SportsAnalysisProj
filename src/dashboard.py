# Build Streamlit dashboard

# run venv/Scripts/activate   
# run streamlit run src/dashboard.py
# run deactivate to stop venv


import streamlit as st
import pandas as pd
from supabase import create_client
from pathlib import Path
import os
from dotenv import load_dotenv

# Load from parent of current script (project root)
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


st.set_page_config(page_title="NBA Stats Dashboard")

data = supabase.table("nba_player_stats_ex").select("*").execute().data
df = pd.DataFrame(data)


player = st.selectbox("Select player", df["name"].unique())
st.write(df[df["name"] == player])

