import pandas as pd
from pathlib import Path
def create_model_data(df):
    # drop these columns since a lot of values are missing
    processed_df = df.drop(columns=['loser_seed', 'winner_entry', 'loser_entry', 'winner_seed'])
    # drop matches with no recorded stats
    processed_df = processed_df.dropna(subset=['w_ace'])
    # fill with meadian the categories that are missing just a couple hundred values, and that wont matter too match in elo calculation
    cols_tofill = ['winner_ht', 'loser_ht', 'winner_age', 'loser_age', 'winner_rank', 'loser_rank']
    processed_df[cols_tofill] = processed_df[cols_tofill].fillna(processed_df[cols_tofill].median())


    #FOR NOW ONLY USING THIS SIMPLIFIED DATABASE
    selected_cols = [
        "winner_name",
        "loser_name",
        "winner_rank",
        "loser_rank",
        "winner_age",
        "loser_age",
        "surface",
        "best_of"
    ]
    
    data = processed_df[selected_cols].copy()

    return data
