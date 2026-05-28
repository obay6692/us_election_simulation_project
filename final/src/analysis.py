# src/analysis.py
import pandas as pd

def analyze_simulation_results(results):
    avg_dem = sum(results["Democrat"]) / len(results["Democrat"])
    avg_rep = sum(results["Republican"]) / len(results["Republican"])
    dem_wins = sum(1 for ev in results["Democrat"] if ev >= 270)
    rep_wins = sum(1 for ev in results["Republican"] if ev >= 270)
    total = len(results["Democrat"])

    return {
        "Average Democratic EV": avg_dem,
        "Average Republican EV": avg_rep,
        "Democratic Win Probability (%)": (dem_wins / total) * 100,
        "Republican Win Probability (%)": (rep_wins / total) * 100,
        "Democratic Wins": dem_wins,
        "Republican Wins": rep_wins,
    }

def identify_swing_states(state_wins):
    swing_states = {}
    for state, results in state_wins.items():
        total = results["Democrat"] + results["Republican"]
        dem_prob = (results["Democrat"] / total) * 100 if total > 0 else 0
        if 40 <= dem_prob <= 60:
            swing_states[state] = {
                "Democrat Win %": dem_prob,
                "Republican Win %": 100 - dem_prob
            }
    return pd.DataFrame(swing_states).T.sort_values(by="Democrat Win %", ascending=False).round(1)
