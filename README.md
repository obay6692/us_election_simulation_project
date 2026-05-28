# US Election Simulation Project

A statistical simulation and visualization project for **US presidential elections**, built across three iterations — from early matplotlib prototypes to a polished multi-page **Streamlit** dashboard with Monte Carlo simulation, historical comparison, and interactive maps.

## Repository structure

| Folder | Stage | What's inside |
|--------|-------|---------------|
| [`prototype1/`](prototype1/) | First iteration | Matplotlib-based exploration. Animated GIFs of cumulative line charts, election bars, stacked bars, and a US map. Single script (`prototype1.py`) + a regression comparison PDF. |
| [`prototype2/`](prototype2/) | Second iteration | First Streamlit app. Adds Monte Carlo simulation, histograms of electoral votes, and 2020 county-level results. Backed by `aggregated_state_results.csv` and `election_summary_2008_2020.csv`. |
| [`final/`](final/) | Final project | Multi-page Streamlit dashboard. Modular Python (`load_data`, `preprocess`, `analysis`, `simulation`, `visualization`) and three pages: Simulation Dashboard, Election History Comparison, and Interactive State & Map. |

## Final app — quick start

```bash
cd final
pip install -r requirements.txt
streamlit run src/Home.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

### Pages

- **Simulation Dashboard** — runs Monte Carlo electoral-college simulations and shows win probabilities + swing-state tables.
- **Election History Comparison** — side-by-side comparison of two historical election years.
- **Interactive State & Map** — clickable US map exposing per-state simulation results.

## Data sources

- `2020_US_County_Level_Presidential_Results.csv` (prototype2)
- `aggregated_state_results.csv` — state-level aggregates 2008–2020
- `election_summary_2008_2020.csv` — election-year summaries
- `us_states_sample.geojson` — geographic boundaries for the map view

## Notes

This project was originally developed as part of a statistics course and is independent from the computer-vision coursework — split out here for clarity.
