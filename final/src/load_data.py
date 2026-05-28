import pandas as pd

def load_election_data(filepath):
    """
    Load and clean election data from CSV file.
    """
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower()
    return df