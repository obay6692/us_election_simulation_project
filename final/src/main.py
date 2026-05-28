# src/main.py
from load_data import load_election_data
from preprocess import compute_win_probabilities
from simulation import simulate_elections_with_markov
from analysis import analyze_simulation_results, identify_swing_states
from visualization import (
    plot_win_counts_plotly,
    plot_electoral_distribution_plotly,
    plot_statewise_probabilities
)

# Step 1: Load and preprocess data
file_path = "data/aggregated_state_results.csv"
df = load_election_data(file_path)
prob_df = compute_win_probabilities(df)

# Step 2: Define electoral votes
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

# Step 3: Run simulation
results, state_wins_over_time, national_trend_history = simulate_elections_with_markov(
    prob_df, electoral_votes
)

# Step 4: Analyze results
summary = analyze_simulation_results(results)
swing_states = identify_swing_states(state_wins_over_time)

# Step 5: Print summary and swing states
print("\n📊 Election Summary:")
for k, v in summary.items():
    print(f"{k}: {v:.2f}")

print("\n🔁 Swing States:")
print(swing_states)

# Step 6: Visualize results
plot_win_counts_plotly(results)
plot_electoral_distribution_plotly(results)
df_probs = plot_statewise_probabilities(state_wins_over_time)

print("\n📋 State-by-state probabilities:")
print(df_probs.head())
