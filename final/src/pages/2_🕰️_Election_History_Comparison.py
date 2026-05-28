import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add the correct path to reach the project root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import from src
from src.load_data import load_election_data
from src.us_state_abbrev import abbrev_us_state

# Configure page
st.set_page_config(page_title="🕰️ Historical Election Comparison", layout="wide")
st.title("🕰️ US Presidential Election History Comparison")

# Load election data
df = load_election_data("data/aggregated_state_results.csv")

# Select years for comparison
years = sorted(df['year'].unique())
col1, col2 = st.columns(2)
with col1:
    year1 = st.selectbox("Select First Election Year", years, index=0)
with col2:
    year2 = st.selectbox("Select Second Election Year", years, index=len(years) - 1)

# Filter data by selected years
df1 = df[df['year'] == year1]
df2 = df[df['year'] == year2]

# Pivot data by party for each year
pivot1 = df1.pivot(index='state_name', columns='party', values='votes').fillna(0)
pivot2 = df2.pivot(index='state_name', columns='party', values='votes').fillna(0)

# Ensure both have 'dem' and 'gop' columns
pivot1 = pivot1.reindex(columns=['dem', 'gop'], fill_value=0)
pivot2 = pivot2.reindex(columns=['dem', 'gop'], fill_value=0)

# Calculate vote change between years
diff = (pivot2 - pivot1).reset_index()
diff['Total Change'] = diff['dem'] - diff['gop']
diff['state_abbr'] = diff['state_name'].map(abbrev_us_state)

# 📊 Bar chart of vote shifts
st.subheader("📊 State-by-State Vote Shift")
st.caption("🟦 Positive = Shift toward Democrats · 🟥 Negative = Shift toward Republicans")

fig = px.bar(
    diff.sort_values("Total Change", ascending=False),
    x="state_name",
    y="Total Change",
    color="Total Change",
    color_continuous_scale="RdBu",
    title=f"Net Political Shift by State: {year1} ➝ {year2}"
)
fig.update_layout(xaxis_title="State", yaxis_title="Change (Dem - GOP)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
#### 🧠 What does this chart mean?
- A positive bar means more Democratic votes were gained compared to Republican gains.
- A negative bar indicates a net shift toward Republicans.
- This helps visualize which states swung the most between the two elections.
""")

# 🗺️ Choropleth map of vote shifts
st.subheader("🗺️ Geographic Political Shift (Choropleth Map)")
st.caption("This map visualizes which states became more Democratic or Republican between the selected elections.")

map_fig = px.choropleth(
    diff,
    locations="state_abbr",
    locationmode="USA-states",
    scope="usa",
    color="Total Change",
    color_continuous_scale="RdBu",
    title=f"Statewise Political Shift: {year1} → {year2}"
)
map_fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
st.plotly_chart(map_fig, use_container_width=True)

# 📥 Data download section
st.markdown("### 📥 Download the Results")
csv = diff.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Vote Shift Data",
    data=csv,
    file_name=f"vote_shift_{year1}_{year2}.csv",
    mime="text/csv"
)

# 📌 Summary section
st.markdown("---")
st.markdown("""
### 📌 Summary
This interactive page compares voting shifts across US states between two historical election years.

You can:
- See which states moved left or right.
- Visualize the political swing per state.
- Download the data for further use.
""")
