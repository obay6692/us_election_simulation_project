import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_win_counts_plotly(results):
    st.subheader("📈 Number of Wins in Simulation")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["Democrat", "Republican"],
        y=[
            sum(ev >= 270 for ev in results["Democrat"]),
            sum(ev >= 270 for ev in results["Republican"])
        ],
        marker=dict(color=["blue", "red"])
    ))
    fig_bar.update_layout(
        title="Number of Wins for Each Party During the Simulation",
        xaxis_title="Party",
        yaxis_title="Number of Wins",
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def plot_electoral_distribution_plotly(results):
    st.subheader("📉 Electoral Vote Distribution")
    st.markdown("**The following chart shows the distribution of electoral votes each party received across simulations.**")

    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=results["Democrat"],
        name="Democrat",
        opacity=0.6,
        marker=dict(color="blue")
    ))
    fig_hist.add_trace(go.Histogram(
        x=results["Republican"],
        name="Republican",
        opacity=0.6,
        marker=dict(color="red")
    ))
    fig_hist.update_layout(
        barmode="overlay",
        title="Distribution of Electoral Votes in the Simulation",
        xaxis_title="Number of Electoral Votes",
        yaxis_title="Frequency",
        legend_title="Party",
        shapes=[
            dict(
                type="line",
                x0=270, x1=270, y0=0, y1=1,
                xref='x', yref='paper',
                line=dict(color="black", dash="dash", width=2)
            )
        ]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

def plot_statewise_probabilities(state_wins):
    df_probs = pd.DataFrame({
        state: {
            "Democrat Win %": (state_wins[state]["Democrat"] / sum(state_wins[state].values())) * 100,
            "Republican Win %": (state_wins[state]["Republican"] / sum(state_wins[state].values())) * 100,
        }
        for state in state_wins
    }).T
    df_probs = df_probs.round(1).sort_values("Democrat Win %", ascending=False)
    return df_probs

def plot_choropleth_map(state_probs_df):
    #st.subheader("🗺️ Expected Winning Party by State")
    st.markdown("**This map shows the party expected to win in each state based on win probabilities.**")

    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
        'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
        'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
        'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
        'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
        'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }

    df_map = state_probs_df.copy()
    df_map["Winning Party"] = df_map.apply(
        lambda row: "Democrat" if row["Democrat Win %"] > row["Republican Win %"] else "Republican",
        axis=1
    )
    df_map["Win Probability"] = df_map[["Democrat Win %", "Republican Win %"]].max(axis=1)
    df_map["state"] = df_map.index.map(state_abbrev)

    fig_map = px.choropleth(
        df_map.reset_index(),
        locations="state",
        locationmode="USA-states",
        color="Winning Party",
        hover_name="index",
        hover_data={"Win Probability": ":.1f", "state": False},
        color_discrete_map={"Democrat": "blue", "Republican": "red"},
        scope="usa",
        title="🗺️ Expected Winning Party by State"
    )
    st.plotly_chart(fig_map, use_container_width=True)

def plot_votes_time_series(df):
    st.subheader("📊 Vote Changes Over Time")
    df_summary = df.groupby(["year", "party"])["votes"].sum().reset_index()
    fig = px.line(
        df_summary,
        x="year",
        y="votes",
        color="party",
        markers=True,
        labels={"votes": "Vote Count", "year": "Year", "party": "Party"},
        title="Vote Changes for Each Party from 2008 to 2024"
    )
    st.plotly_chart(fig, use_container_width=True)
