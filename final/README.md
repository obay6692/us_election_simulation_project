
```markdown
# 🇺🇸 US Presidential Election Simulation

This project simulates U.S. presidential election outcomes.  
It provides an interactive Streamlit dashboard with multiple pages to explore simulation results, historical trends, and interactive maps.

---

## ✨ Features

- 📊 Run election simulations and visualize win probabilities  
- 🕰️ Compare results across two historical election years  
- 🗺️ Explore an interactive U.S. map showing simulated outcomes  
- 📥 Download swing state and probability tables as CSV

---

## 📂 Project Structure

```

/data/
aggregated\_state\_results.csv
bar\_chart.gif
election\_bars.gif
state\_probs\_export.csv
us\_map.gif

/src/
analysis.py
load\_data.py
preprocess.py
simulation.py
visualization.py
us\_state\_abbrev.py
Home.py
main.py

/src/pages/
1\_📊\_Simulation\_Dashboard.py
2\_🕰️\_Election\_History\_Comparison.py
3\_🗺️\_Interactive\_Map.py

````

---

## 🚀 How to Run the App

1. Install required libraries:
    ```
    pip install -r requirements.txt
    ```

2. Run the Streamlit app:
    ```
    streamlit run src/Home.py
    ```

3. Navigate between pages using the sidebar:
    - 📊 Simulation Dashboard  
    - 🕰️ Historical Comparison  
    - 🗺️ Interactive Map

---

## 📊 Methods Used

- **Markov Chain Monte Carlo (MCMC)** simulation  
- **Probability distributions** and statistical inference  
- **Monte Carlo simulations** with >10,000 iterations  
- **Visualization tools** using Plotly and Streamlit

---

## 📥 Data Sources

- Kaggle election datasets  
- Federal Election Commission (FEC) results

---

✅ Enjoy exploring U.S. elections!
````

