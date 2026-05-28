# Interactive_state_and_Map.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.load_data import load_election_data
from src.preprocess import compute_win_probabilities
from src.simulation import simulate_elections_with_markov
from src.analysis import analyze_simulation_results, identify_swing_states
from src.visualization import (
    plot_win_counts_plotly,
    plot_electoral_distribution_plotly,
    plot_statewise_probabilities,
    plot_choropleth_map,
    plot_votes_time_series
)

st.set_page_config(layout="wide", page_title="US Election Simulation Dashboard 🇺🇸")
st.title("🗳️ US Presidential Election Simulation")

# --- Load aggregated state data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/aggregated_state_results.csv")

df = load_data()

# --- Sidebar Controls ---
st.sidebar.header("🔎 Controls")
states = df['state_name'].unique()
selected_state = st.sidebar.selectbox("Select a state:", sorted(states))

# --- Filtered State Data ---
state_data = df[df['state_name'] == selected_state]

# --- 1. Votes Distribution Over Years ---
st.subheader(f"📊 Votes Distribution in {selected_state} (2008–2024)")
fig_votes = px.bar(
    state_data,
    x='year', y='votes',
    color='party',
    barmode='group',
    title=f"Number of Votes by Party in {selected_state} (2008–2024)",
    labels={"votes": "Number of Votes", "year": "Year", "party": "Party"}
)
st.plotly_chart(fig_votes, use_container_width=True)
st.caption("This chart shows the total number of votes for each party over the election years in the selected state.")

# --- 2. Voting Changes ---
pivot = state_data.pivot(index='year', columns='party', values='votes').fillna(0)
pivot['dem_change'] = pivot['dem'].diff()
pivot['gop_change'] = pivot['gop'].diff()

st.subheader("📈 Vote Changes Between Elections")
fig_swing = px.bar(
    pivot.reset_index(),
    x='year', y=['dem_change', 'gop_change'],
    barmode='group',
    title="Vote Changes (Democrats vs Republicans)",
    labels={"value": "Vote Change", "year": "Year"}
)
st.plotly_chart(fig_swing, use_container_width=True)
st.caption("This chart illustrates the change in votes for Democrats and Republicans between consecutive elections.")

# --- 3. Standard Deviation and RSD ---
st.subheader("📉 Voting Volatility (Standard Deviation and RSD)")
summary = state_data.groupby('party')['votes'].agg(['mean', 'std']).reset_index()
summary['RSD (%)'] = (summary['std'] / summary['mean']) * 100

fig_std = px.bar(
    summary, x='party', y='std',
    title="Standard Deviation by Party",
    labels={"std": "Standard Deviation"}
)
st.plotly_chart(fig_std, use_container_width=True)
st.caption("This chart displays the standard deviation of votes, indicating how much vote counts vary across elections.")

fig_rsd = px.bar(
    summary, x='party', y='RSD (%)',
    title="Relative Standard Deviation (RSD) by Party",
    labels={"RSD (%)": "RSD (%)"}
)
st.plotly_chart(fig_rsd, use_container_width=True)
st.caption("This chart shows the relative standard deviation (RSD), expressing variability as a percentage of the mean.")

# --- 4. 2028 Election Prediction ---
st.subheader(f"🔮 2028 Election Prediction in {selected_state}")
latest = pivot.iloc[-1]
avg_change = pivot[['dem_change', 'gop_change']].mean()
pred_dem = latest['dem'] + avg_change['dem_change']
pred_gop = latest['gop'] + avg_change['gop_change']
winner = "Democratic" if pred_dem > pred_gop else "Republican"
st.markdown(f"### 🧠 Predicted Winner in 2028: *{winner}*")
st.caption("Based on average past vote changes, this section predicts which party is more likely to win in the next election.")

# --- 5. Run Simulation for All States + Choropleth Map ---
st.subheader("🗺️ State-Level Map: Win Probabilities and Predicted Winner")

@st.cache_data
def run_simulation_for_map():
    df_sim = load_election_data("data/aggregated_state_results.csv")
    prob_df = compute_win_probabilities(df_sim)

    electoral_votes = {
        'Alabama': 9, 'Alaska': 3, 'Arizona': 11, 'Arkansas': 6, 'California': 55,
        'Colorado': 9, 'Connecticut': 7, 'Delaware': 3, 'Florida': 29, 'Georgia': 16,
        'Hawaii': 4, 'Idaho': 4, 'Illinois': 20, 'Indiana': 11, 'Iowa': 6, 'Kansas': 6,
        'Kentucky': 8, 'Louisiana': 8, 'Maine': {'statewide': 2, 'districts': [1, 1]},
        'Maryland': 10, 'Massachusetts': 11, 'Michigan': 16, 'Minnesota': 10,
        'Mississippi': 6, 'Missouri': 10, 'Montana': 3, 'Nebraska': {'statewide': 2, 'districts': [1, 1, 1]},
        'Nevada': 6, 'New Hampshire': 4, 'New Jersey': 14, 'New Mexico': 5,
        'New York': 29, 'North Carolina': 15, 'North Dakota': 3, 'Ohio': 18,
        'Oklahoma': 7, 'Oregon': 7, 'Pennsylvania': 20, 'Rhode Island': 4,
        'South Carolina': 9, 'South Dakota': 3, 'Tennessee': 11, 'Texas': 38,
        'Utah': 6, 'Vermont': 3, 'Virginia': 13, 'Washington': 12, 'West Virginia': 5,
        'Wisconsin': 10, 'Wyoming': 3, 'District of Columbia': 3
    }

    _, state_wins, _ = simulate_elections_with_markov(prob_df, electoral_votes, 10000)
    state_probs_df = plot_statewise_probabilities(state_wins)
    return state_probs_df

state_probs_df = run_simulation_for_map()
plot_choropleth_map(state_probs_df)
st.caption("This interactive map shows the probability of each party winning in each state based on the simulation.")

# --- Footer ---
st.markdown("---")
st.markdown("📊 Data sourced from the Federal Election Commission (FEC) and simulated using Monte Carlo and Markov Chains in Python.")
