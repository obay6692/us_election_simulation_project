import numpy as np
import pandas as pd

def simulate_elections_with_markov(prob_df, electoral_votes, num_simulations=10000):
    results = {"Democrat": [], "Republican": []}
    national_trend_history = []
    state_wins_over_time = {state: {"Democrat": 0, "Republican": 0} for state in electoral_votes}

    transition_matrix = {
        "Democrat": {"Democrat": 0.85, "Republican": 0.15},
        "Republican": {"Democrat": 0.15, "Republican": 0.85}
    }

    state_probabilities = {}
    for _, row in prob_df.iterrows():
        state = row['state_name']
        party = row['party']
        prob = row['win_probability']
        if state not in state_probabilities:
            state_probabilities[state] = {}
        state_probabilities[state][party] = prob

    current_trend = "Democrat"

    for _ in range(num_simulations):
        trend_probs = transition_matrix[current_trend]
        current_trend = np.random.choice(list(trend_probs.keys()), p=list(trend_probs.values()))
        national_trend_history.append(current_trend)

        vote_count = {"Democrat": 0, "Republican": 0}

        for state, parties in state_probabilities.items():
            dem_prob = parties.get('dem', 0.5)
            rep_prob = parties.get('rep', 0.5)

            if current_trend == "Democrat":
                dem_prob *= 1.02
                rep_prob *= 0.98
            else:
                dem_prob *= 0.98
                rep_prob *= 1.02

            total = dem_prob + rep_prob
            dem_prob /= total
            rep_prob /= total

            winner = np.random.choice(["Democrat", "Republican"], p=[dem_prob, rep_prob])

            ev = electoral_votes.get(state, 0)
            if isinstance(ev, dict):
                vote_count[winner] += ev['statewide']
                for district_votes in ev['districts']:
                    district_winner = np.random.choice(["Democrat", "Republican"], p=[dem_prob, rep_prob])
                    vote_count[district_winner] += district_votes
            else:
                vote_count[winner] += ev

            state_wins_over_time[state][winner] += 1

        results["Democrat"].append(vote_count["Democrat"])
        results["Republican"].append(vote_count["Republican"])

    return results, state_wins_over_time, national_trend_history