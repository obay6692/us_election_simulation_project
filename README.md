# U.S. Presidential Election Simulation Project

> Final project for **MA-223-G 25V Statistikk** — Faculty of Engineering and Science, University of Agder, Grimstad, May 2025.

A statistical simulation of U.S. presidential election outcomes built from five cycles of historical state-level voting data (2008, 2012, 2016, 2020, 2024). The model combines **Monte Carlo simulation** with **Markov chains** to capture both state-level uncertainty and correlated national swings, then presents the results through an interactive multi-page **Streamlit** dashboard.

The project is purely data-driven — it does not weigh political events, polling, or current news. It asks one question: *given how each state has actually voted over the last five elections, what is the distribution of plausible 2028 outcomes?*

## Repository structure

| Folder | Stage | What's inside |
|--------|-------|---------------|
| [`prototype1/`](prototype1/) | First iteration | Matplotlib exploration — animated GIFs of cumulative line charts, election bars, stacked bars, and a US map. Single script + a regression-comparison PDF. |
| [`prototype2/`](prototype2/) | Second iteration | First Streamlit version. Adds the Monte Carlo simulation, histograms of electoral votes, and 2020 county-level results. |
| [`final/`](final/) | **Final submission** | Multi-page Streamlit dashboard with a modular `src/` layout (`load_data`, `preprocess`, `simulation`, `analysis`, `visualization`) and four pages. |

## The final dashboard

Four pages, each tied to a different statistical question:

1. **Home** — project overview and entry point.
2. **Simulation Dashboard** — runs the Monte Carlo engine and shows win probabilities, expected electoral votes, and downloadable swing-state tables.
3. **Historical Comparison** — net political shift bar charts and choropleth maps comparing any two election cycles (2008–2024).
4. **Interactive State and Map** — clickable U.S. map with per-state win probabilities and hover-level vote differentials.

## Methodology

### Data pipeline

State-level election results from 2008 through 2024 are aggregated from county-level data ([tonmcg/US_County_Level_Election_Results_08-24](https://github.com/tonmcg/US_County_Level_Election_Results_08-24) and Kaggle).

`load_data.py` reads the per-state CSVs and standardizes column names. `preprocess.py` then derives **empirical per-state win probabilities** from those historical aggregations — these are the priors the simulation engine draws from.

The unified output lives in `final/data/aggregated_state_results.csv`.

### Simulation engine (`simulation.py`)

For each simulated election:

1. Draw each state's winner from its empirical probability distribution.
2. Apply a **Markov transition** representing national momentum, so correlated swings (a wave year) emerge naturally instead of states being treated as independent.
3. Handle **split allocation** in Maine and Nebraska at the district level.
4. Tally electoral votes and record the national outcome.

Repeated thousands of times, this produces a posterior distribution over outcomes — not a single prediction, but a range of plausible scenarios with associated probabilities.

### Analysis (`analysis.py`)

Aggregates the simulation runs to compute:

- National win probability per party
- Expected and credible-interval electoral-vote totals
- **Swing-state flags** — states with a 40–60% win probability for either party

### Visualization (`visualization.py`)

Powered by Plotly:

- Choropleth maps with the standard blue/red political color convention
- Histograms of electoral-vote outcomes per party
- Animated bar charts of net political shifts between cycles
- Hover tooltips for exact vote differentials

## Statistical methods used

| Measure | Implementation | Reference (Nyberg, *Statistikk: en bayesiansk tilnærming*, 2nd ed.) |
|---------|----------------|---------------------------------------------------------------------|
| Bayesian predictive mean | `np.mean(simulations, axis=0)` | Ch. 13.2, 13.3 |
| Standard deviation | `np.std(simulations, axis=0)` | Ch. 2.4 |
| Predictive probability | `np.mean(results == "Biden")` | Ch. 13.2, 13.3 |
| Beta distribution | `beta(α + wins, β + losses)` | Ch. 10.5, 13.2 |
| Monte Carlo simulation | Thousands of randomized runs | Ch. 13.2, 14.2.2 |
| Expected value | `np.sum(probabilities * electoral_votes)` | Ch. 7.5 |
| Normal approximation | Large-sample voting-distribution approx. | Ch. 10 |
| Credible intervals | `np.percentile(simulations, [2.5, 97.5], axis=0)` | Ch. 15.3 |

## Key findings

Across **10,000 simulated elections**:

- Democratic candidates win on average **294.2 electoral votes**; Republicans **243.8**
- Democrats prevail in **~68.9%** of simulations; Republicans in **~30.4%**
- Distribution shapes differ: Democratic outcomes cluster above the 270-vote threshold, while Republican outcomes show wider spread and mostly fall below it
- Third-party support shows the highest **relative standard deviation**, meaning the most volatility relative to its mean
- The Upper Midwest (WI, MI, PA) consistently emerges as the most volatile region; the South (AL, MS) the most stable Republican; western growth states (AZ, CO) trend Democratic
- California showed the strongest 2008–2020 Democratic shift; Ohio the strongest Republican shift

## Running the final app

The app is designed to run in an Anaconda environment.

```bash
cd final
pip install -r requirements.txt
streamlit run src/Home.py
```

Streamlit will open at `http://localhost:8501`. Navigate the four pages from the sidebar.

### Tech stack

- **Python** — core language
- **Pandas** — data cleaning and aggregation
- **NumPy** — simulation math
- **Streamlit** — interactive web dashboard
- **Plotly** — interactive charts and choropleth maps
- **Anaconda** — recommended runtime environment

## References

1. *US_County_Level_Election_Results_08-24* — [github.com/tonmcg/US_County_Level_Election_Results_08-24](https://github.com/tonmcg/US_County_Level_Election_Results_08-24)
2. *Kaggle Election Datasets* — [kaggle.com/datasets?search=election](https://www.kaggle.com/datasets?search=election)
3. *Anaconda Distribution* — [anaconda.com/download](https://www.anaconda.com/download)
4. S. O. Nyberg, *Statistikk: en bayesiansk tilnærming*, 2nd ed. Oslo: Universitetsforlaget, 2017. ISBN 978-82-15-02637-4.

## License & academic context

Coursework submitted for MA-223-G 25V Statistikk at the University of Agder. Released here for portfolio and reproducibility purposes.
