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
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

# Load from parent of current script (project root)
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# Page config
st.set_page_config(page_title="NBA Stats Dashboard")

st.title("NBA Player Stats Viewer")

# Supabase table data (if needed)
data = supabase.table("nba_player_stats_ex").select("*").execute().data
if data:
    df_supabase = pd.DataFrame(data)
    player_from_supabase = st.selectbox("Select player from Supabase", df_supabase["name"].unique())
    st.write(df_supabase[df_supabase["name"] == player_from_supabase])

st.header("Get Live Stats via NBA API")

# NBA API player list
player_dict = players.get_players()
player_names = sorted([player["full_name"] for player in player_dict])

selected_player = st.selectbox("Select a player (NBA API)", player_names)

if selected_player:
    player_id = [p for p in player_dict if p["full_name"] == selected_player][0]["id"]
    season = st.selectbox("Select season", ["2023", "2022", "2021"])

    try:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df_api = gamelog.get_data_frames()[0]

        st.subheader(f"{selected_player} - Game Log ({season})")
        st.dataframe(df_api)

        # Optional: Show some summary stats
        st.subheader("Stat Summary")
        st.write(df_api.describe()[["PTS", "AST", "REB", "FG_PCT"]])

        # Optional: Chart example
        st.line_chart(df_api[["PTS", "AST", "REB"]].iloc[::-1].reset_index(drop=True))

    except Exception as e:
        st.error(f"Failed to fetch data for {selected_player}: {e}")

