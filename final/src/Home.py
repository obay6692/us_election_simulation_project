import streamlit as st

st.set_page_config(page_title="🏠 Home", layout="wide")

st.title("🏛️ US Presidential Election Simulation Project")

st.markdown("""
Welcome to the **US Presidential Election Simulation**!
""")
st.markdown("""
This project simulates and analyzes U.S. presidential election outcomes using statistical models based on historical data. It highlights electoral shifts and explores their potential impact on both state-level results and national outcomes.

In this app, you can:
- 📊 Run election simulations and view predictions.
- 🕰️ Compare historical elections across years.
- 🗺️ Explore an interactive state and map.
""")


st.subheader("Navigate to:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Simulation Dashboard"):
        st.switch_page("pages/1_📊_Simulation_Dashboard.py")

with col2:
    if st.button("🕰️ Historical Comparison"):
        st.switch_page("pages/2_🕰️_Election_History_Comparison.py")

with col3:
    if st.button("🗺️ Interactive State and Map"):
        st.switch_page("pages/3_🗺️_Interactive_state_and_Map.py")


# 🔥 Add GIFs here
#st.subheader("Project Highlights")
st.image("data/election_bars.gif", caption="Election Results Animation", use_container_width=True)
st.image("data/us_map.gif", caption="US Map with Predicted Winners", use_container_width=True)

st.markdown("---")
st.markdown("Developed as part of the **US Presidential Election Simulation Project** 📈🇺🇸")
