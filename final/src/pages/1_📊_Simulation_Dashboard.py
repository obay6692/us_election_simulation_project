# src/simulation_Dashboard.py
import streamlit as st
import plotly.graph_objects as go
import time
import random
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

num_simulations = st.sidebar.slider("🔁 Number of Simulations", 1000, 20000, 10000, 1000)
if st.sidebar.button("🔄 Rerun Simulation"):
    st.rerun()

@st.cache_data
def run_simulation(num_simulations):
    df = load_election_data("data/aggregated_state_results.csv")
    prob_df = compute_win_probabilities(df)

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

    results, state_wins, trend = simulate_elections_with_markov(prob_df, electoral_votes, num_simulations)
    summary = analyze_simulation_results(results)
    swing_states = identify_swing_states(state_wins)
    state_probs_df = plot_statewise_probabilities(state_wins)
    return results, summary, swing_states, state_probs_df

results, summary, swing_states_df, state_probs_df = run_simulation(num_simulations)

# --- Simulation Summary ---
st.subheader("🌟 Simulation Summary")
st.metric("Average Democratic EV", f"{summary['Average Democratic EV']:.1f}")
st.metric("Average Republican EV", f"{summary['Average Republican EV']:.1f}")
st.metric("Democratic Win Probability", f"{summary['Democratic Win Probability (%)']:.1f}%")
st.metric("Republican Win Probability", f"{summary['Republican Win Probability (%)']:.1f}%")
st.caption("This section shows the average electoral votes (EV) and the win probabilities for both parties based on the simulation results.")

# --- Win Counts Plot ---
plot_win_counts_plotly(results)
st.caption("This plot shows how many times each party won the election across all simulations.")

# --- Electoral Vote Distribution Plot ---
plot_electoral_distribution_plotly(results)
st.caption("This chart displays the distribution of electoral votes for Democrats and Republicans across all simulations.")

# --- Swing States Table ---
st.subheader("🔁 Swing States")
st.dataframe(swing_states_df)
st.caption("This table lists the swing states — those with the closest margins and highest uncertainty in the simulation results.")
st.download_button("⬇️ Download Swing States Table", swing_states_df.to_csv().encode(), "swing_states.csv")

# --- State-by-State Win Probabilities ---
st.subheader("📋 State-by-State Win Probabilities")
st.dataframe(state_probs_df)
st.caption("This table shows the win probabilities for each party in every state, based on simulation outcomes.")
st.download_button("⬇️ Download State Probabilities", state_probs_df.to_csv().encode(), "state_probabilities.csv")
state_probs_df.to_csv("data/state_probs_export.csv", index=False)

# --- Historical Vote Trends ---
df_all = load_election_data("data/aggregated_state_results.csv")
plot_votes_time_series(df_all)
st.caption("This time series chart visualizes the historical vote trends by party across all states from 2008 to 2024.")

# --- Interactive Election Simulation Map ---
st.subheader("🗺️ Interactive Election Simulation")
run = st.button("Run Simulation")
speed = st.slider("Simulation Speed (seconds per state)", 0.1, 2.0, 0.5, 0.1)
st.caption("Press 'Run Simulation' to visualize a random live simulation of the election, state by state, with accumulating electoral votes.")

states_ev = {
    'CA': 55, 'TX': 38, 'FL': 29, 'NY': 29, 'PA': 20, 'IL': 20, 'OH': 18, 'GA': 16,
    'NC': 15, 'MI': 16, 'NJ': 14, 'VA': 13, 'WA': 12, 'AZ': 11, 'IN': 11, 'MA': 11,
    'TN': 11, 'MO': 10, 'MD': 10, 'WI': 10, 'MN': 10, 'CO': 9, 'AL': 9, 'SC': 9,
    'KY': 8, 'LA': 8, 'CT': 7, 'OK': 7, 'OR': 7, 'AR': 6, 'IA': 6, 'KS': 6, 'MS': 6,
    'NV': 6, 'UT': 6, 'NE': 5, 'NM': 5, 'WV': 5, 'HI': 4, 'ID': 4, 'ME': 4, 'NH': 4,
    'RI': 4, 'MT': 3, 'DE': 3, 'SD': 3, 'ND': 3, 'AK': 3, 'DC': 3, 'VT': 3, 'WY': 3
}

map_placeholder = st.empty()
dem_ev, rep_ev = 0, 0
colors = {}

if run:
    for state, votes in states_ev.items():
        winner = random.choice(['Democrat', 'Republican'])
        colors[state] = 'blue' if winner == 'Democrat' else 'red'
        if winner == 'Democrat':
            dem_ev += votes
        else:
            rep_ev += votes

        fig = go.Figure(data=go.Choropleth(
            locations=list(colors.keys()),
            z=[1 if c == 'blue' else 0 for c in colors.values()],
            locationmode='USA-states',
            colorscale=[(0, "red"), (1, "blue")],
            showscale=False
        ))
        fig.update_layout(
            geo_scope='usa',
            title=f"Electoral Vote Count: Democrat {dem_ev} - Republican {rep_ev}"
        )
        map_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(speed)

st.markdown("---")
st.markdown("This project uses Monte Carlo Simulation and Markov Chains to model U.S. election results.")
