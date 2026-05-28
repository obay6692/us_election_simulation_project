# المتطلبات: geopandas, matplotlib, pillow

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Patch

# تحميل خريطة الولايات من مصدر موثوق
states_map = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")

# 1. إنشاء بيانات الانتخابات
states = ["California", "Texas", "Florida", "New York", "Pennsylvania", "Ohio", "Georgia", "Michigan", "North Carolina", "Arizona", "Wisconsin", "Nevada", "Minnesota", "Virginia"]

electoral_votes = {"California": 55, "Texas": 38, "Florida": 29, "New York": 29, "Pennsylvania": 20, "Ohio": 18, "Georgia": 16, "Michigan": 16, "North Carolina": 15, "Arizona": 11, "Wisconsin": 10, "Nevada": 6, "Minnesota": 10, "Virginia": 13}

data = []
years = [2008, 2012, 2016, 2020]
dem_base = [60, 58, 48, 51]
rep_base = [38, 40, 50, 48]

for i, year in enumerate(years):
    for state in states:
        dem = dem_base[i] + np.random.uniform(-5, 5)
        rep = rep_base[i] + np.random.uniform(-5, 5)
        total = dem + rep
        data.append({
            'year': year,
            'state': state,
            'dem_pct': round(dem / total * 100, 1),
            'rep_pct': round(rep / total * 100, 1),
            'electoral_votes': electoral_votes[state]
        })

df = pd.DataFrame(data)

# 2. المحاكاة وتسجيل النتائج
num_simulations = 100
results_by_year = {year: {"Democrat": 0, "Republican": 0} for year in years}
state_results = {year: {state: [] for state in states} for year in years}

for year in years:
    df_year = df[df['year'] == year]
    for i in range(num_simulations):
        dem_total = 0
        rep_total = 0
        for _, row in df_year.iterrows():
            p_dem = row['dem_pct'] / (row['dem_pct'] + row['rep_pct'])
            winner = np.random.choice(['Democrat', 'Republican'], p=[p_dem, 1 - p_dem])
            state_results[year][row['state']].append(winner)
            if winner == 'Democrat':
                dem_total += row['electoral_votes']
            else:
                rep_total += row['electoral_votes']
        if dem_total > rep_total:
            results_by_year[year]['Democrat'] += 1
        else:
            results_by_year[year]['Republican'] += 1

# 3. إعداد بيانات الخريطة
frames_data = []
for year in years:
    for i in range(num_simulations):
        frame = {'year': year, 'frame': i}
        for state in states:
            frame[state] = state_results[year][state][i]
        frames_data.append(frame)

df_frames = pd.DataFrame(frames_data)

# ضبط أسماء الولايات
states_map['name'] = states_map['name'].replace({
    'District of Columbia': 'District of Columbia',
    'New York': 'New York',
    'Texas': 'Texas',
    'Florida': 'Florida',
    'California': 'California',
    'Pennsylvania': 'Pennsylvania',
    'Ohio': 'Ohio',
    'Georgia': 'Georgia',
    'Michigan': 'Michigan',
    'North Carolina': 'North Carolina',
    'Arizona': 'Arizona',
    'Wisconsin': 'Wisconsin',
    'Nevada': 'Nevada',
    'Minnesota': 'Minnesota',
    'Virginia': 'Virginia'
})

# 4. أنيميشن خريطة الولايات المتحدة
fig1, ax1 = plt.subplots(figsize=(10, 6))
def update_map(frame):
    ax1.clear()
    year = years[frame // num_simulations]
    i = frame % num_simulations
    data = df_frames[(df_frames['year'] == year) & (df_frames['frame'] == i)].iloc[0]
    states_map['color'] = states_map['name'].apply(lambda x: 'blue' if data.get(x) == 'Democrat' else ('red' if data.get(x) == 'Republican' else 'lightgray'))
    states_map.plot(color=states_map['color'], edgecolor='black', ax=ax1)
    ax1.set_title(f"Simulated Election Map - Year: {year} | Simulation: {i+1}")
    ax1.axis('off')
    legend_elements = [Patch(facecolor='blue', label='Democrat'), Patch(facecolor='red', label='Republican')]
    ax1.legend(handles=legend_elements, loc='lower left')

map_anim = FuncAnimation(fig1, update_map, frames=len(years)*num_simulations, interval=100)
map_anim.save("us_election_map.gif", writer="pillow", fps=10)
plt.close(fig1)

# 5. أنيميشن Bar Chart لعدد مرات الفوز
fig2, ax2 = plt.subplots(figsize=(8, 5))
bar_years = []
dem_wins = []
rep_wins = []

for year in years:
    bar_years.append(year)
    dem_wins.append(results_by_year[year]['Democrat'])
    rep_wins.append(results_by_year[year]['Republican'])

def update_bar(frame):
    ax2.clear()
    current_years = years[:frame+1]
    ax2.bar(current_years, dem_wins[:frame+1], label='Democrat', color='blue')
    ax2.bar(current_years, rep_wins[:frame+1], bottom=dem_wins[:frame+1], label='Republican', color='red')
    ax2.set_title("Simulated Wins by Party")
    ax2.set_ylabel("Wins")
    ax2.set_xlabel("Year")
    ax2.legend()

bar_anim = FuncAnimation(fig2, update_bar, frames=len(years), interval=1000)
bar_anim.save("election_bars.gif", writer="pillow", fps=1)
plt.close(fig2)

print("GIFs saved: 'us_election_map.gif' and 'election_bars.gif'")