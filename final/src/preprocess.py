import pandas as pd

def compute_win_probabilities(df):
    """
    Compute the win probability for each party in each state based on historical data.
    Returns a DataFrame with state, party, and win_probability.
    """
    winners = df.sort_values('votes', ascending=False).drop_duplicates(subset=['state_name', 'year'])
    win_counts = winners.groupby(['state_name', 'party']).size().reset_index(name='wins')
    total_elections = winners.groupby('state_name').size().reset_index(name='total')
    win_probs = pd.merge(win_counts, total_elections, on='state_name')
    win_probs['win_probability'] = win_probs['wins'] / win_probs['total']
    return win_probs[['state_name', 'party', 'win_probability']]