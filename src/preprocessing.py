import pandas as pd
import numpy as np
from pathlib import Path
def create_model_data(data):
    # drop these columns since a lot of values are missing
    processed_data = data.drop(columns=['loser_seed', 'winner_entry', 'loser_entry', 'winner_seed'])
    # drop matches with no recorded stats
    #processed_data = processed_data.dropna(subset=['w_ace'])
    # fill with meadian the categories that are missing just a couple hundred values, and that wont matter too match in elo calculation
    #cols_tofill = ['winner_ht', 'loser_ht', 'winner_age', 'loser_age', 'winner_rank', 'loser_rank']
    #processed_data[cols_tofill] = processed_data[cols_tofill].fillna(processed_data[cols_tofill].median())


    #FOR NOW ONLY USING THIS SIMPLIFIED DATABASE
    selected_cols = [
        "winner_name",
        "winner_id",
        "loser_name",
        "loser_id",
        "winner_rank",
        "loser_rank",
        "winner_age",
        "loser_age",
        "surface",
        "best_of"
    ]
    
    data = processed_data[selected_cols].copy()

    np.random.seed(1)
    orientation = np.random.randint(0, 2, size=len(data))
    # If orientation == 1, player_1 is winner
    # If orientation == 0, player_1 is loser
    data["target"] = orientation

    data["player_1_id"] = np.where(data["target"] == 1, data["winner_id"], data["loser_id"])
    data["player_1_name"] = np.where(data["target"] == 1, data["winner_name"], data["loser_name"])
    data["player_1_rank"] = np.where(data["target"] == 1, data["winner_rank"], data["loser_rank"])
    data["player_1_age"] = np.where(data["target"] == 1, data["winner_age"], data["loser_age"])

    data["player_2_id"] = np.where(data["target"] == 1, data["loser_id"], data["winner_id"])
    data["player_2_name"] = np.where(data["target"] == 1, data["loser_name"], data["winner_name"])
    data["player_2_rank"] = np.where(data["target"] == 1, data["loser_rank"], data["winner_rank"])
    data["player_2_age"] = np.where(data["target"] == 1, data["loser_age"], data["winner_age"])

    # Difference features
    data["rank_diff"] = data["player_1_rank"] - data["player_2_rank"]
    data["age_diff"] = data["player_1_age"] - data["player_2_age"]

    # Final clean dataframe
    final_cols = [
        "player_1_id",
        "player_1_name",
        "player_2_id",
        "player_2_name",
        "player_1_rank",
        "player_2_rank",
        "player_1_age",
        "player_2_age",
        "rank_diff",
        "age_diff",
        "surface",
        "best_of",
        "target"
    ]
    
    # Drop rows with missing values in critical columns
    data = data.dropna(subset=["player_1_rank", "player_2_rank","player_1_age", "player_2_age", "rank_diff", "age_diff", "surface"])

    clean_data = data[final_cols].copy()

    return clean_data
